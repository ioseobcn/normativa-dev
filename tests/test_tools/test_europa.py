"""Tests para leer_norma_ue y el parser DOUE."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

from normativa.tools.europa import _normalizar_segmento, leer_norma_ue
from normativa.xml_parser import parse_doue, render_doue_segmento

# Estructura real de www.boe.es/buscar/xml.php?id=DOUE-... (reducida).
_DOUE_XML = (
    "<documento>"
    "<metadatos>"
    "<identificador>DOUE-L-2024-81079</identificador>"
    "<titulo>Reglamento (UE) 2024/1689 (AI Act)</titulo>"
    "<rango>Reglamento</rango>"
    "<numero_oficial>1689/2024</numero_oficial>"
    "<fecha_publicacion>20240712</fecha_publicacion>"
    "<fecha_vigencia>20240801</fecha_vigencia>"
    "<url_eli>https://data.europa.eu/eli/reg/2024/1689/spa</url_eli>"
    "</metadatos>"
    "<analisis>"
    "<materias><materia>Inteligencia artificial</materia></materias>"
    "<notas><nota>Aplicable desde el 2 de agosto de 2026.</nota></notas>"
    "</analisis>"
    "<texto>"
    '<p class="parrafo">EL PARLAMENTO EUROPEO Y EL CONSEJO...</p>'
    '<p class="articulo">Artículo 1</p>'
    '<p class="parrafo">Objeto</p>'
    '<p class="parrafo">1.  El objetivo del presente Reglamento...</p>'
    '<p class="articulo">Artículo 2</p>'
    '<p class="parrafo">Ámbito de aplicación</p>'
    '<p class="parrafo">1.  El presente Reglamento se aplica...</p>'
    '<p class="anexo_num">ANEXO I</p>'
    '<p class="anexo_tit">Lista de actos legislativos</p>'
    "<table><tbody><tr><td>Celda A</td><td>Celda B</td></tr></tbody></table>"
    "</texto>"
    "</documento>"
)


class TestParseDoue:
    def test_metadatos_y_analisis(self):
        parsed = parse_doue(_DOUE_XML)
        assert parsed["metadatos"]["identificador"] == "DOUE-L-2024-81079"
        assert parsed["analisis"]["materias"] == ["Inteligencia artificial"]
        assert "2 de agosto de 2026" in parsed["analisis"]["notas"][0]

    def test_segmenta_articulos_y_anexos(self):
        parsed = parse_doue(_DOUE_XML)
        ids = [s["id"] for s in parsed["segmentos"]]
        assert ids == ["preambulo", "a1", "a2", "anexoi"]

    def test_titulo_incluye_rubrica(self):
        parsed = parse_doue(_DOUE_XML)
        a1 = next(s for s in parsed["segmentos"] if s["id"] == "a1")
        assert a1["titulo"] == "Artículo 1. Objeto"

    def test_render_segmento_con_tabla(self):
        parsed = parse_doue(_DOUE_XML)
        anexo = next(s for s in parsed["segmentos"] if s["id"] == "anexoi")
        md = render_doue_segmento(anexo)
        assert "## ANEXO I" in md
        assert "| Celda A | Celda B |" in md


class TestNormalizarSegmento:
    def test_variantes(self):
        assert _normalizar_segmento("5") == "a5"
        assert _normalizar_segmento("articulo 5") == "a5"
        assert _normalizar_segmento("Artículo 113") == "a113"
        assert _normalizar_segmento("anexo III") == "anexoiii"
        assert _normalizar_segmento("anexo 4") == "anexoiv"
        assert _normalizar_segmento("preambulo") == "preambulo"


class TestLeerNormaUe:
    async def _run(self, **kwargs):
        with patch("normativa.tools.europa.get_client", new_callable=AsyncMock) as mock_gc, \
             patch("normativa.tools.europa.get_cache", new_callable=AsyncMock) as mock_cc:
            mock_client = AsyncMock()
            mock_client.doue_documento.return_value = _DOUE_XML
            mock_gc.return_value = mock_client

            mock_cache = AsyncMock()
            async def passthrough_fetch(table, key, fn, **kw):
                return await fn()
            mock_cache.get_or_fetch.side_effect = passthrough_fetch
            mock_cc.return_value = mock_cache

            return await leer_norma_ue(**kwargs)

    async def test_indice_sin_articulo(self):
        result = await self._run(doue_id="DOUE-L-2024-81079")
        assert "error" not in result
        assert result["total_segmentos"] == 4
        assert result["indice"][1]["titulo"] == "Artículo 1. Objeto"

    async def test_articulo_concreto(self):
        result = await self._run(doue_id="DOUE-L-2024-81079", articulo="articulo 2")
        assert result["segmento"] == "a2"
        assert "se aplica" in result["texto"]
        assert result["nota_vigencia"]

    async def test_celex_mapeado_en_dominios(self):
        result = await self._run(doue_id="32024R1689")
        assert "error" not in result
        assert result["doue_id"] == "DOUE-L-2024-81079"

    async def test_segmento_inexistente_sugiere(self):
        result = await self._run(doue_id="DOUE-L-2024-81079", articulo="99")
        assert "error" in result
        assert "a1" in result["segmentos_disponibles"]

    async def test_id_invalido(self):
        result = await leer_norma_ue("BOE-A-2015-11430")
        assert "error" in result
