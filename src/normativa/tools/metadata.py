"""Herramientas de metadatos y analisis de disposiciones BOE."""

from __future__ import annotations

from typing import Any

from normativa.tools._shared import get_client, get_cache


async def obtener_metadatos(boe_id: str) -> dict[str, Any]:
    """Obtiene los metadatos completos de una disposicion del BOE.

    Parametros:
    - boe_id: identificador BOE (ej: "BOE-A-2006-20764")

    Devuelve: titulo, rango, fecha_publicacion, departamento, estado de
    consolidacion, materias, url ELI, y otros metadatos disponibles.
    """
    try:
        if not boe_id or not boe_id.startswith("BOE"):
            return {"error": f"boe_id invalido: '{boe_id}'. Debe empezar por 'BOE-'.", "tool": "obtener_metadatos"}

        client = await get_client()
        cache = await get_cache()
        data = await cache.get_or_fetch(
            "metadatos", boe_id, lambda: client.legislacion_metadatos(boe_id)
        )

        # Aplanar: la API devuelve {"status":..., "data": [item]} o {"status":..., "data": {...}}
        raw = data.get("data", data) if isinstance(data, dict) else data
        # Si es lista, tomar el primer elemento
        if isinstance(raw, list):
            meta = raw[0] if raw else {}
        else:
            meta = raw

        return {"boe_id": boe_id, "data": meta} if isinstance(meta, dict) else {"boe_id": boe_id, "raw": meta}

    except Exception as exc:
        return {"error": str(exc), "tool": "obtener_metadatos", "boe_id": boe_id}


async def obtener_analisis(
    boe_id: str,
    incluir_referencias: bool = True,
    max_referencias: int = 20,
) -> dict[str, Any]:
    """Obtiene el analisis juridico de una disposicion: materias y referencias cruzadas.

    Parametros:
    - boe_id: identificador BOE (ej: "BOE-A-2006-20764")
    - incluir_referencias: si incluir normas que afecta/es afectada por (default True)
    - max_referencias: limite de referencias por tipo (default 20)

    Devuelve: materias, notas, referencias (afecta_a, afectada_por) con sus
    identificadores y descripcion.
    """
    try:
        if not boe_id or not boe_id.startswith("BOE"):
            return {"error": f"boe_id invalido: '{boe_id}'. Debe empezar por 'BOE-'.", "tool": "obtener_analisis"}

        client = await get_client()
        cache = await get_cache()
        data = await cache.get_or_fetch(
            "analisis", boe_id, lambda: client.legislacion_analisis(boe_id)
        )

        analisis = data.get("data", data) if isinstance(data, dict) else data

        resultado: dict[str, Any] = {"boe_id": boe_id}

        if isinstance(analisis, dict):
            # Materias
            if "materias" in analisis:
                resultado["materias"] = analisis["materias"]

            # Notas
            if "notas" in analisis:
                resultado["notas"] = analisis["notas"]

            # Referencias cruzadas
            if incluir_referencias:
                for tipo_ref in ("afecta_a", "afectada_por", "referencias"):
                    if tipo_ref in analisis:
                        refs = analisis[tipo_ref]
                        if isinstance(refs, list):
                            resultado[tipo_ref] = refs[:max_referencias]
                            if len(refs) > max_referencias:
                                resultado[f"{tipo_ref}_total"] = len(refs)
                                resultado[f"{tipo_ref}_truncado"] = True
                        else:
                            resultado[tipo_ref] = refs

        return resultado

    except Exception as exc:
        return {"error": str(exc), "tool": "obtener_analisis", "boe_id": boe_id}
