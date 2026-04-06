"""Tests for normativa.tools.metadata — obtener_metadatos and obtener_analisis."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

from normativa.tools.metadata import obtener_metadatos, obtener_analisis


# ---------------------------------------------------------------------------
# obtener_metadatos
# ---------------------------------------------------------------------------


class TestObtenerMetadatos:
    """Test obtener_metadatos tool."""

    async def test_invalid_boe_id_returns_error(self):
        """Non-BOE ID should return error dict, not raise exception."""
        result = await obtener_metadatos("INVALID-ID-123")
        assert "error" in result
        assert "tool" in result
        assert result["tool"] == "obtener_metadatos"

    async def test_empty_boe_id_returns_error(self):
        """Empty string should return error dict."""
        result = await obtener_metadatos("")
        assert "error" in result

    async def test_valid_response_parsed_correctly(self, sample_metadatos_json):
        """Valid API response should be parsed into structured result."""
        with patch("normativa.tools.metadata.get_client", new_callable=AsyncMock) as mock_gc, \
             patch("normativa.tools.metadata.get_cache", new_callable=AsyncMock) as mock_cc:

            mock_client = AsyncMock()
            mock_client.legislacion_metadatos.return_value = sample_metadatos_json
            mock_gc.return_value = mock_client

            mock_cache = AsyncMock()
            # Make cache.get_or_fetch call the fetch_fn
            async def passthrough_fetch(table, key, fn, **kwargs):
                return await fn()
            mock_cache.get_or_fetch.side_effect = passthrough_fetch
            mock_cc.return_value = mock_cache

            result = await obtener_metadatos("BOE-A-2014-12328")

        assert "error" not in result
        assert result["boe_id"] == "BOE-A-2014-12328"
        assert "data" in result
        data = result["data"]
        assert data["titulo"] == "Ley 27/2014, de 27 de noviembre, del Impuesto sobre Sociedades"
        assert data["rango"] == "Ley"
        assert data["estado_consolidacion"] == "Vigente"

    async def test_api_error_returns_error_dict(self):
        """API exception should be caught and returned as error dict."""
        with patch("normativa.tools.metadata.get_client", new_callable=AsyncMock) as mock_gc, \
             patch("normativa.tools.metadata.get_cache", new_callable=AsyncMock) as mock_cc:

            mock_client = AsyncMock()
            mock_client.legislacion_metadatos.side_effect = ConnectionError("timeout")
            mock_gc.return_value = mock_client

            mock_cache = AsyncMock()
            async def passthrough_fetch(table, key, fn, **kwargs):
                return await fn()
            mock_cache.get_or_fetch.side_effect = passthrough_fetch
            mock_cc.return_value = mock_cache

            result = await obtener_metadatos("BOE-A-2014-12328")

        assert "error" in result
        assert "boe_id" in result


# ---------------------------------------------------------------------------
# obtener_analisis
# ---------------------------------------------------------------------------


class TestObtenerAnalisis:
    """Test obtener_analisis tool."""

    async def test_invalid_boe_id_returns_error(self):
        """Non-BOE ID should return error dict."""
        result = await obtener_analisis("INVALID")
        assert "error" in result
        assert result["tool"] == "obtener_analisis"

    async def test_valid_response_includes_materias(self):
        """Valid response should include materias from analysis."""
        analisis_response = {
            "status": "OK",
            "data": {
                "materias": ["Impuestos", "Impuesto sobre Sociedades"],
                "notas": "Texto consolidado.",
                "afecta_a": [
                    {"identificador": "BOE-A-2004-4456", "titulo": "RDLeg 4/2004", "tipo": "Deroga"}
                ],
                "afectada_por": [
                    {"identificador": "BOE-A-2022-23042", "titulo": "Ley 28/2022", "tipo": "Modifica"}
                ],
            },
        }

        with patch("normativa.tools.metadata.get_client", new_callable=AsyncMock) as mock_gc, \
             patch("normativa.tools.metadata.get_cache", new_callable=AsyncMock) as mock_cc:

            mock_client = AsyncMock()
            mock_client.legislacion_analisis.return_value = analisis_response
            mock_gc.return_value = mock_client

            mock_cache = AsyncMock()
            async def passthrough_fetch(table, key, fn, **kwargs):
                return await fn()
            mock_cache.get_or_fetch.side_effect = passthrough_fetch
            mock_cc.return_value = mock_cache

            result = await obtener_analisis("BOE-A-2014-12328")

        assert "error" not in result
        assert result["boe_id"] == "BOE-A-2014-12328"
        assert "materias" in result
        assert "Impuestos" in result["materias"]
        assert "afecta_a" in result
        assert "afectada_por" in result

    async def test_max_referencias_truncation(self):
        """References should be truncated to max_referencias."""
        many_refs = [{"identificador": f"BOE-A-{i}", "titulo": f"Ley {i}"} for i in range(30)]
        analisis_response = {
            "status": "OK",
            "data": {
                "materias": ["Test"],
                "afecta_a": many_refs,
            },
        }

        with patch("normativa.tools.metadata.get_client", new_callable=AsyncMock) as mock_gc, \
             patch("normativa.tools.metadata.get_cache", new_callable=AsyncMock) as mock_cc:

            mock_client = AsyncMock()
            mock_client.legislacion_analisis.return_value = analisis_response
            mock_gc.return_value = mock_client

            mock_cache = AsyncMock()
            async def passthrough_fetch(table, key, fn, **kwargs):
                return await fn()
            mock_cache.get_or_fetch.side_effect = passthrough_fetch
            mock_cc.return_value = mock_cache

            result = await obtener_analisis(
                "BOE-A-2014-12328", max_referencias=5
            )

        assert len(result["afecta_a"]) == 5
        assert result["afecta_a_total"] == 30
        assert result["afecta_a_truncado"] is True

    async def test_without_referencias(self):
        """When incluir_referencias=False, no refs in output."""
        analisis_response = {
            "status": "OK",
            "data": {
                "materias": ["Test"],
                "afecta_a": [{"identificador": "BOE-A-0001", "titulo": "Test"}],
            },
        }

        with patch("normativa.tools.metadata.get_client", new_callable=AsyncMock) as mock_gc, \
             patch("normativa.tools.metadata.get_cache", new_callable=AsyncMock) as mock_cc:

            mock_client = AsyncMock()
            mock_client.legislacion_analisis.return_value = analisis_response
            mock_gc.return_value = mock_client

            mock_cache = AsyncMock()
            async def passthrough_fetch(table, key, fn, **kwargs):
                return await fn()
            mock_cache.get_or_fetch.side_effect = passthrough_fetch
            mock_cc.return_value = mock_cache

            result = await obtener_analisis(
                "BOE-A-2014-12328", incluir_referencias=False
            )

        assert "afecta_a" not in result
        assert "materias" in result
