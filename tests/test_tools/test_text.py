"""Tests para normalizacion de bloque_id e historial de versiones."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

from normativa.tools.text import _normalizar_bloque_id, historial_versiones

_XML = (
    '<response status="OK"><data>'
    '<bloque id="a48" tipo="precepto" titulo="Articulo 48.">'
    '<version id_norma="BOE-A-2015-11430" fecha_publicacion="20151024" fecha_vigencia="20151113">'
    '<p class="parrafo">Redaccion original.</p>'
    "</version>"
    '<version id_norma="BOE-A-2024-25523" fecha_publicacion="20241206" fecha_vigencia="20241206">'
    '<p class="parrafo">Redaccion vigente.</p>'
    "</version>"
    "</bloque>"
    "</data></response>"
)


class TestNormalizarBloqueId:
    def test_numero_a_secas(self):
        assert _normalizar_bloque_id("56") == "a56"

    def test_articulo_con_palabra(self):
        assert _normalizar_bloque_id("articulo 56") == "a56"
        assert _normalizar_bloque_id("Art. 56") == "a56"
        assert _normalizar_bloque_id("artículo 13 bis") == "a13bis"

    def test_id_boe_intacto(self):
        assert _normalizar_bloque_id("a56") == "a56"
        assert _normalizar_bloque_id("dfquinta") == "dfquinta"
        assert _normalizar_bloque_id("tpreliminar") == "tpreliminar"


class TestHistorialVersiones:
    async def _run(self, **kwargs):
        with patch("normativa.tools.text.get_client", new_callable=AsyncMock) as mock_gc, \
             patch("normativa.tools.text.get_cache", new_callable=AsyncMock) as mock_cc:
            mock_client = AsyncMock()
            mock_client.legislacion_bloque.return_value = _XML
            mock_gc.return_value = mock_client

            mock_cache = AsyncMock()
            async def passthrough_fetch(table, key, fn, **kw):
                return await fn()
            mock_cache.get_or_fetch.side_effect = passthrough_fetch
            mock_cc.return_value = mock_cache

            return await historial_versiones("BOE-A-2015-11430", **kwargs)

    async def test_lista_versiones_marcando_vigente(self):
        result = await self._run(bloque_id="48")
        assert result["num_versiones"] == 2
        vigentes = [v for v in result["versiones"] if v["vigente"]]
        assert len(vigentes) == 1
        assert vigentes[0]["id_norma"] == "BOE-A-2024-25523"
        assert "texto" not in result

    async def test_texto_de_version_historica(self):
        result = await self._run(bloque_id="a48", fecha_vigencia="20151113")
        assert "original" in result["texto"]
        assert result["version_solicitada"]["id_norma"] == "BOE-A-2015-11430"

    async def test_boe_id_invalido(self):
        result = await historial_versiones("INVALID", "a1")
        assert "error" in result
