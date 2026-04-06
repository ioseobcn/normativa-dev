"""Async HTTP client for the BOE open data API."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)

BASE_URL = "https://www.boe.es/datosabiertos/api"

_MAX_RETRIES = 3
_BACKOFF_BASE = 1.0
_TIMEOUT = 30.0
_MAX_RPS = 2  # max requests per second


class BOEClient:
    """Thin async wrapper around the BOE datos abiertos REST API.

    Use as an async context manager::

        async with BOEClient() as boe:
            meta = await boe.legislacion_metadatos("BOE-A-2006-20764")
    """

    def __init__(self) -> None:
        self._client: httpx.AsyncClient | None = None
        self._semaphore = asyncio.Semaphore(_MAX_RPS)

    # -- context manager --------------------------------------------------

    async def __aenter__(self) -> BOEClient:
        self._client = httpx.AsyncClient(
            base_url=BASE_URL,
            timeout=_TIMEOUT,
            headers={"Accept": "application/json"},
        )
        return self

    async def __aexit__(self, *exc: object) -> None:
        await self.close()

    async def close(self) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    # -- internal helpers -------------------------------------------------

    async def _request(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        accept: str = "application/json",
    ) -> httpx.Response:
        """GET *path* with retry + exponential backoff + rate limiting."""
        if self._client is None:
            raise RuntimeError("BOEClient is not open. Use 'async with BOEClient() as c:'")

        last_exc: Exception | None = None
        for attempt in range(1, _MAX_RETRIES + 1):
            async with self._semaphore:
                try:
                    resp = self._client.build_request(
                        "GET",
                        path,
                        params=params,
                        headers={"Accept": accept},
                    )
                    response = await self._client.send(resp)
                    response.raise_for_status()
                    # Rate-limit: space requests at least 0.5 s apart.
                    await asyncio.sleep(1.0 / _MAX_RPS)
                    return response
                except httpx.HTTPStatusError as exc:
                    # 4xx errors are client errors — retrying won't help
                    if exc.response.status_code < 500:
                        raise
                    last_exc = exc
                    delay = _BACKOFF_BASE * (2 ** (attempt - 1))
                    logger.warning(
                        "BOE request %s failed (attempt %d/%d): %s — retrying in %.1fs",
                        path,
                        attempt,
                        _MAX_RETRIES,
                        exc,
                        delay,
                    )
                    await asyncio.sleep(delay)
                except httpx.TransportError as exc:
                    last_exc = exc
                    delay = _BACKOFF_BASE * (2 ** (attempt - 1))
                    logger.warning(
                        "BOE request %s failed (attempt %d/%d): %s — retrying in %.1fs",
                        path,
                        attempt,
                        _MAX_RETRIES,
                        exc,
                        delay,
                    )
                    await asyncio.sleep(delay)

        raise last_exc  # type: ignore[misc]

    async def _get_json(self, path: str, **params: Any) -> dict:
        params = {k: v for k, v in params.items() if v is not None}
        resp = await self._request(path, params=params or None)
        return resp.json()

    async def _get_xml(self, path: str) -> str:
        resp = await self._request(path, accept="application/xml")
        return resp.text

    # -- public API -------------------------------------------------------

    async def legislacion_lista(
        self,
        limit: int = 10,
        offset: int = 0,
        from_date: str | None = None,
        to_date: str | None = None,
        query: str | None = None,
    ) -> dict:
        """List legislation matching optional filters.

        Dates use YYYYMMDD format.
        """
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if query:
            params["query"] = query
        resp = await self._request("/legislacion-consolidada", params=params)
        return resp.json()

    async def legislacion_metadatos(self, boe_id: str) -> dict:
        """Fetch metadata for a specific BOE disposition."""
        return await self._get_json(f"/legislacion-consolidada/id/{boe_id}/metadatos")

    async def legislacion_analisis(self, boe_id: str) -> dict:
        """Fetch legal analysis (afecta / afectado por) for a disposition."""
        return await self._get_json(f"/legislacion-consolidada/id/{boe_id}/analisis")

    async def legislacion_indice(self, boe_id: str) -> list[dict]:
        """Fetch the article index of a consolidated text."""
        data = await self._get_json(f"/legislacion-consolidada/id/{boe_id}/texto/indice")
        # The API wraps the list under a key; return the inner list.
        if isinstance(data, dict):
            return data.get("data", data.get("items", [data]))
        return data  # type: ignore[return-value]

    async def legislacion_bloque(self, boe_id: str, bloque_id: str) -> str:
        """Fetch a single text block (article / section) as raw XML."""
        return await self._get_xml(
            f"/legislacion-consolidada/id/{boe_id}/texto/bloque/{bloque_id}"
        )

    async def sumario_boe(self, fecha: str) -> dict:
        """Fetch the BOE daily summary for *fecha* (YYYYMMDD)."""
        return await self._get_json(f"/boe/sumario/{fecha}")

    async def sumario_borme(self, fecha: str) -> dict:
        """Fetch the BORME daily summary for *fecha* (YYYYMMDD)."""
        return await self._get_json(f"/borme/sumario/{fecha}")

    async def datos_auxiliares(self, tipo: str) -> dict:
        """Fetch auxiliary reference data.

        *tipo* is one of: ``materias``, ``departamentos``, ``rangos``, ``ambitos``.
        """
        valid = {"materias", "departamentos", "rangos", "ambitos"}
        if tipo not in valid:
            raise ValueError(f"tipo must be one of {valid}, got {tipo!r}")
        return await self._get_json(f"/datos-auxiliares/{tipo}")
