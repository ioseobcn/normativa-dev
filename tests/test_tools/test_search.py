"""Tests for normativa.tools.search — buscar_por_dominio and buscar_legislacion."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

from normativa.tools.search import buscar_por_dominio, buscar_legislacion


# ---------------------------------------------------------------------------
# buscar_por_dominio
# ---------------------------------------------------------------------------


class TestBuscarPorDominio:
    """Test buscar_por_dominio tool."""

    async def test_returns_leyes_clave_for_fiscal(self):
        """Fiscal domain should include leyes_clave from the DomainConfig."""
        # buscar_por_dominio calls get_client which hits BOE API.
        # Mock get_client to avoid HTTP. The tool falls back to registry data.
        with patch("normativa.tools.search.get_client", new_callable=AsyncMock) as mock_gc:
            mock_client = AsyncMock()
            mock_client.legislacion_lista.side_effect = ConnectionError("mocked offline")
            mock_gc.return_value = mock_client

            result = await buscar_por_dominio(dominio="fiscal")

        assert "error" not in result
        assert result["dominio"] == "fiscal"
        assert "leyes_clave" in result
        assert len(result["leyes_clave"]) == 4
        boe_ids = [l["boe_id"] for l in result["leyes_clave"]]
        assert "BOE-A-2006-20764" in boe_ids  # IRPF
        assert "BOE-A-1992-28740" in boe_ids  # IVA

    async def test_eu_refs_included_in_output(self):
        """EU references should be present for leyes that have them."""
        with patch("normativa.tools.search.get_client", new_callable=AsyncMock) as mock_gc:
            mock_client = AsyncMock()
            mock_client.legislacion_lista.side_effect = ConnectionError("mocked offline")
            mock_gc.return_value = mock_client

            result = await buscar_por_dominio(dominio="fiscal")

        # IVA law has an EU directive ref
        leyes_with_eu = [
            l for l in result.get("leyes_clave", []) if "eu_refs" in l
        ]
        assert len(leyes_with_eu) >= 2  # IVA + IS (ATAD)
        iva_ley = next(
            (l for l in leyes_with_eu if l["boe_id"] == "BOE-A-1992-28740"), None
        )
        assert iva_ley is not None
        assert iva_ley["eu_refs"][0]["celex"] == "32006L0112"

    async def test_cross_domain_search_by_caso_uso(self):
        """Search without specifying dominio, using caso_uso text."""
        with patch("normativa.tools.search.get_client", new_callable=AsyncMock) as mock_gc:
            mock_client = AsyncMock()
            mock_client.legislacion_lista.side_effect = ConnectionError("mocked offline")
            mock_gc.return_value = mock_client

            result = await buscar_por_dominio(caso_uso="cookies RGPD")

        # Should auto-detect a domain (proteccion_datos or digital)
        assert "error" not in result
        assert result.get("dominio") in ("proteccion_datos", "digital")

    async def test_invalid_domain_returns_error(self):
        """Non-existent domain should return error dict, not exception."""
        result = await buscar_por_dominio(dominio="nonexistent_xyz")
        assert "error" in result
        assert "tool" in result
        assert result["tool"] == "buscar_por_dominio"
        assert "dominios_disponibles" in result

    async def test_empty_params_returns_error(self):
        """No domain, no caso_uso, no subtema should return error."""
        result = await buscar_por_dominio()
        assert "error" in result
        assert "dominios_disponibles" in result

    async def test_laboral_domain_works(self):
        """Laboral domain should load and return results."""
        with patch("normativa.tools.search.get_client", new_callable=AsyncMock) as mock_gc:
            mock_client = AsyncMock()
            mock_client.legislacion_lista.side_effect = ConnectionError("mocked offline")
            mock_gc.return_value = mock_client

            result = await buscar_por_dominio(dominio="laboral")

        assert "error" not in result
        assert result["dominio"] == "laboral"
        assert "leyes_clave" in result


# ---------------------------------------------------------------------------
# buscar_legislacion
# ---------------------------------------------------------------------------


class TestBuscarLegislacion:
    """Test buscar_legislacion tool."""

    async def test_fallback_to_registry_on_api_error(self):
        """When BOE API fails, should fall back to local registry."""
        with patch("normativa.tools.search.get_client", new_callable=AsyncMock) as mock_gc:
            mock_client = AsyncMock()
            mock_client.legislacion_lista.side_effect = ConnectionError("mocked offline")
            mock_gc.return_value = mock_client

            result = await buscar_legislacion(query="IRPF")

        assert "error" not in result
        assert result.get("fuente") == "registro_local"
        assert len(result["resultados"]) >= 1

    async def test_with_mock_api_success(self):
        """When BOE API succeeds, should return API results."""
        with patch("normativa.tools.search.get_client", new_callable=AsyncMock) as mock_gc:
            mock_client = AsyncMock()
            mock_client.legislacion_lista.return_value = {
                "total": 1,
                "data": [
                    {
                        "identificador": "BOE-A-2006-20764",
                        "titulo": "Ley 35/2006 del IRPF",
                        "rango": "Ley",
                        "fecha_publicacion": "20061129",
                        "estado_consolidacion": "Vigente",
                    }
                ],
            }
            mock_gc.return_value = mock_client

            result = await buscar_legislacion(query="IRPF")

        assert "error" not in result
        assert result["total"] == 1
        assert result["resultados"][0]["boe_id"] == "BOE-A-2006-20764"

    async def test_limit_capped_at_50(self):
        """Limit should be capped at 50 even if user requests more."""
        with patch("normativa.tools.search.get_client", new_callable=AsyncMock) as mock_gc:
            mock_client = AsyncMock()
            mock_client.legislacion_lista.return_value = {"total": 0, "data": []}
            mock_gc.return_value = mock_client

            result = await buscar_legislacion(query="test", limit=100)

        assert result["limit"] == 50
