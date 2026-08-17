"""Tests para las herramientas de sumarios BOE/BORME."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

from normativa.tools.summary import (
    _extraer_entradas_sumario,
    _fecha_a_yyyymmdd,
    sumario_boe,
)


def _sumario_real() -> dict:
    """Estructura real de GET /boe/sumario/{fecha} (reducida).

    Los nodos con un solo hijo vienen como dict en vez de lista
    (conversion XML->JSON del BOE).
    """
    return {
        "status": {"code": "200", "text": "ok"},
        "data": {
            "sumario": {
                "metadatos": {"publicacion": "BOE", "fecha_publicacion": "20260814"},
                "diario": [{
                    "numero": "199",
                    "sumario_diario": {"identificador": "BOE-S-2026-199"},
                    "seccion": [
                        {
                            "codigo": "1",
                            "nombre": "I. Disposiciones generales",
                            "departamento": [{
                                "codigo": "7723",
                                "nombre": "MINISTERIO DE HACIENDA",
                                "epigrafe": {
                                    # dict (un solo epigrafe), item dict (un solo item)
                                    "nombre": "Impuestos",
                                    "item": {
                                        "identificador": "BOE-A-2026-11111",
                                        "titulo": "Orden por la que se modifica el IRPF",
                                        "url_pdf": {"szBytes": "1", "texto": "https://boe.es/x.pdf"},
                                        "url_html": "https://boe.es/y",
                                    },
                                },
                            }],
                        },
                        {
                            "codigo": "5A",
                            "nombre": "V. Anuncios",
                            "departamento": [{
                                "codigo": "1",
                                "nombre": "MINISTERIO DE DEFENSA",
                                # seccion V: items directamente bajo departamento
                                "item": [
                                    {"identificador": "BOE-B-2026-22222", "titulo": "Anuncio de licitacion"},
                                    {"identificador": "BOE-B-2026-33333", "titulo": "Otro anuncio"},
                                ],
                            }],
                        },
                    ],
                }],
            },
        },
    }


class TestExtraerEntradas:
    def test_aplana_jerarquia_completa(self):
        entradas = _extraer_entradas_sumario(_sumario_real())
        assert len(entradas) == 3
        ids = [e["boe_id"] for e in entradas]
        assert "BOE-A-2026-11111" in ids
        assert "BOE-B-2026-22222" in ids

    def test_conserva_contexto_de_la_rama(self):
        entradas = _extraer_entradas_sumario(_sumario_real())
        primera = next(e for e in entradas if e["boe_id"] == "BOE-A-2026-11111")
        assert primera["departamento"] == "MINISTERIO DE HACIENDA"
        assert primera["epigrafe"] == "Impuestos"
        assert primera["seccion"].startswith("1 ")
        assert primera["url_pdf"] == "https://boe.es/x.pdf"

    def test_items_bajo_departamento_sin_epigrafe(self):
        entradas = _extraer_entradas_sumario(_sumario_real())
        anuncio = next(e for e in entradas if e["boe_id"] == "BOE-B-2026-22222")
        assert anuncio["departamento"] == "MINISTERIO DE DEFENSA"
        assert anuncio["epigrafe"] == ""

    def test_envelope_vacio(self):
        assert _extraer_entradas_sumario({}) == []
        assert _extraer_entradas_sumario({"data": {}}) == []


class TestSumarioBoe:
    async def test_filtro_departamento(self):
        with patch("normativa.tools.summary.get_client", new_callable=AsyncMock) as mock_gc, \
             patch("normativa.tools.summary.get_cache", new_callable=AsyncMock) as mock_cc:
            mock_client = AsyncMock()
            mock_client.sumario_boe.return_value = _sumario_real()
            mock_gc.return_value = mock_client

            mock_cache = AsyncMock()
            async def passthrough_fetch(table, key, fn, **kwargs):
                return await fn()
            mock_cache.get_or_fetch.side_effect = passthrough_fetch
            mock_cc.return_value = mock_cache

            result = await sumario_boe(fecha="20260814", departamento="hacienda")

        assert "error" not in result
        assert result["total"] == 1
        assert result["entradas"][0]["boe_id"] == "BOE-A-2026-11111"


class TestFecha:
    def test_formatos_flexibles(self):
        assert _fecha_a_yyyymmdd("2026-08-14") == "20260814"
        assert _fecha_a_yyyymmdd("14/08/2026") == "20260814"
        assert _fecha_a_yyyymmdd("20260814") == "20260814"
