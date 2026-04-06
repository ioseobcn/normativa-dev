"""Shared fixtures for normativa tests."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest


# ---------------------------------------------------------------------------
# XML fixtures — real BOE bloque samples
# ---------------------------------------------------------------------------


@pytest.fixture()
def sample_bloque_xml() -> str:
    """Real XML from Art. 29 Ley del Impuesto sobre Sociedades (LIS)."""
    return (
        '<response status="OK">'
        "<data>"
        '<bloque id="a29" tipo="precepto" titulo="Articulo 29. Tipo de gravamen.">'
        '<version id_norma="BOE-A-2014-12328" '
        'fecha_publicacion="20141128" fecha_vigencia="20150101">'
        '<p class="articulo">Articulo 29. Tipo de gravamen.</p>'
        '<p class="parrafo">1. El tipo general de gravamen para los '
        "contribuyentes de este Impuesto sera del 25 por ciento.</p>"
        '<p class="parrafo_2">No obstante, las entidades de nueva creacion '
        "que realicen actividades economicas tributaran, en el primer "
        "periodo impositivo en que la base imponible resulte positiva y "
        "en el siguiente, al tipo del 15 por ciento.</p>"
        '<p class="parrafo">2. Tributaran al tipo del 20 por ciento las '
        "cooperativas fiscalmente protegidas.</p>"
        "</version>"
        "</bloque>"
        "</data>"
        "</response>"
    )


@pytest.fixture()
def sample_bloque_xml_empty() -> str:
    """A bloque with no <p> elements inside."""
    return (
        '<bloque id="da1" tipo="disposicion" titulo="Disposicion adicional primera.">'
        '<version id_norma="BOE-A-2014-12328" '
        'fecha_publicacion="20141128" fecha_vigencia="20150101">'
        "</version>"
        "</bloque>"
    )


@pytest.fixture()
def sample_bloque_xml_no_version() -> str:
    """A bloque without a <version> element (edge case)."""
    return (
        '<bloque id="a1" tipo="precepto" titulo="Articulo 1.">'
        '<p class="articulo">Articulo 1. Naturaleza del impuesto.</p>'
        '<p class="parrafo">El Impuesto sobre Sociedades es un tributo '
        "de caracter directo y naturaleza personal.</p>"
        "</bloque>"
    )


@pytest.fixture()
def sample_bloque_xml_multi_class() -> str:
    """A bloque with paragraphs using different CSS classes."""
    return (
        '<bloque id="a15" tipo="precepto" titulo="Articulo 15.">'
        '<version id_norma="BOE-A-2014-12328" '
        'fecha_publicacion="20141128" fecha_vigencia="20150101">'
        '<p class="articulo">Articulo 15. Gastos no deducibles.</p>'
        '<p class="parrafo">No tendran la consideracion de gastos '
        "fiscalmente deducibles:</p>"
        '<p class="parrafo_2">a) Los que representen una retribucion '
        "de los fondos propios.</p>"
        '<p class="parrafo_2">b) Los derivados de la contabilizacion '
        "del Impuesto sobre Sociedades.</p>"
        '<p class="parrafo_3">Se incluyen en esta letra las multas y '
        "sanciones.</p>"
        '<p class="parrafo">Los gastos anteriores no seran deducibles '
        "en ningun caso.</p>"
        "</version>"
        "</bloque>"
    )


# ---------------------------------------------------------------------------
# JSON fixtures — real BOE API response shapes
# ---------------------------------------------------------------------------


@pytest.fixture()
def sample_metadatos_json() -> dict:
    """Real JSON shape from GET /legislacion-consolidada/id/{id}/metadatos."""
    return {
        "status": "OK",
        "data": {
            "identificador": "BOE-A-2014-12328",
            "titulo": (
                "Ley 27/2014, de 27 de noviembre, del Impuesto sobre Sociedades"
            ),
            "rango": "Ley",
            "numero_oficial": "27/2014",
            "fecha_publicacion": "20141128",
            "fecha_vigencia": "20150101",
            "estado_consolidacion": "Vigente",
            "departamento": "Jefatura del Estado",
            "url_eli": (
                "https://www.boe.es/eli/es/l/2014/11/27/27/con"
            ),
            "materias": ["Impuestos", "Impuesto sobre Sociedades"],
            "origen_legislativo": "Estatal",
            "notas": "Ultima actualizacion publicada 01/01/2024",
        },
    }


@pytest.fixture()
def sample_indice_json() -> dict:
    """Real JSON shape from GET /legislacion-consolidada/id/{id}/texto/indice."""
    return {
        "status": "OK",
        "data": {
            "items": [
                {
                    "id": "tpreliminar",
                    "titulo": "Titulo Preliminar. Naturaleza y ambito de aplicacion",
                    "fecha_actualizacion": "20240101",
                },
                {
                    "id": "a1",
                    "titulo": "Articulo 1. Naturaleza",
                    "fecha_actualizacion": "20240101",
                },
                {
                    "id": "a4",
                    "titulo": "Articulo 4. Hecho imponible",
                    "fecha_actualizacion": "20240101",
                },
                {
                    "id": "a7",
                    "titulo": "Articulo 7. Sujeto pasivo",
                    "fecha_actualizacion": "20240101",
                },
                {
                    "id": "a10",
                    "titulo": "Articulo 10. Concepto y determinacion de la base imponible",
                    "fecha_actualizacion": "20240101",
                },
                {
                    "id": "a29",
                    "titulo": "Articulo 29. Tipo de gravamen",
                    "fecha_actualizacion": "20240101",
                },
            ],
        },
    }


# ---------------------------------------------------------------------------
# Mock BOE client — returns fixtures without HTTP calls
# ---------------------------------------------------------------------------


@pytest.fixture()
def mock_boe_client(sample_metadatos_json, sample_indice_json, sample_bloque_xml):
    """Async mock of BOEClient that returns fixture data."""
    client = AsyncMock()
    client.legislacion_metadatos.return_value = sample_metadatos_json
    client.legislacion_analisis.return_value = {
        "status": "OK",
        "data": {
            "materias": ["Impuestos", "Impuesto sobre Sociedades"],
            "notas": "Texto consolidado vigente.",
            "afecta_a": [
                {
                    "identificador": "BOE-A-2004-4456",
                    "titulo": "Real Decreto Legislativo 4/2004",
                    "tipo": "Deroga",
                }
            ],
            "afectada_por": [
                {
                    "identificador": "BOE-A-2022-23042",
                    "titulo": "Ley 28/2022",
                    "tipo": "Modifica",
                }
            ],
        },
    }
    client.legislacion_indice.return_value = sample_indice_json["data"]["items"]
    client.legislacion_bloque.return_value = sample_bloque_xml
    client.legislacion_lista.return_value = {
        "status": "OK",
        "total": 1,
        "data": [
            {
                "identificador": "BOE-A-2014-12328",
                "titulo": "Ley 27/2014, del Impuesto sobre Sociedades",
                "rango": "Ley",
                "fecha_publicacion": "20141128",
                "estado_consolidacion": "Vigente",
            }
        ],
    }
    client.sumario_boe.return_value = {"status": "OK", "data": {}}
    client.sumario_borme.return_value = {"status": "OK", "data": {}}
    client.datos_auxiliares.return_value = {"status": "OK", "data": []}
    return client
