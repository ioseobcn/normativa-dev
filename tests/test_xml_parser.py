"""Tests for normativa.xml_parser — BOE XML to Markdown conversion."""

from __future__ import annotations

import pytest

from normativa.xml_parser import parse_bloque, parse_indice


# ---------------------------------------------------------------------------
# parse_bloque
# ---------------------------------------------------------------------------


class TestParseBloqueNormal:
    """Test parse_bloque with a well-formed article XML."""

    def test_extracts_bloque_id(self, sample_bloque_xml):
        result = parse_bloque(sample_bloque_xml)
        assert result["id"] == "a29"

    def test_extracts_tipo(self, sample_bloque_xml):
        result = parse_bloque(sample_bloque_xml)
        assert result["tipo"] == "precepto"

    def test_extracts_titulo(self, sample_bloque_xml):
        result = parse_bloque(sample_bloque_xml)
        assert result["titulo"] == "Articulo 29. Tipo de gravamen."

    def test_extracts_version_info(self, sample_bloque_xml):
        result = parse_bloque(sample_bloque_xml)
        assert result["version"]["id_norma"] == "BOE-A-2014-12328"
        assert result["version"]["fecha_publicacion"] == "20141128"
        assert result["version"]["fecha_vigencia"] == "20150101"

    def test_converts_articulo_class_to_heading(self, sample_bloque_xml):
        result = parse_bloque(sample_bloque_xml)
        assert "## Articulo 29. Tipo de gravamen." in result["texto_markdown"]

    def test_includes_paragraph_content(self, sample_bloque_xml):
        result = parse_bloque(sample_bloque_xml)
        assert "25 por ciento" in result["texto_markdown"]

    def test_includes_indented_content(self, sample_bloque_xml):
        result = parse_bloque(sample_bloque_xml)
        # parrafo_2 should be indented with 2 spaces
        assert "  No obstante" in result["texto_markdown"]


class TestParseBloqueEmpty:
    """Test parse_bloque with an empty bloque (no paragraphs)."""

    def test_returns_empty_markdown(self, sample_bloque_xml_empty):
        result = parse_bloque(sample_bloque_xml_empty)
        assert result["texto_markdown"] == ""

    def test_preserves_metadata(self, sample_bloque_xml_empty):
        result = parse_bloque(sample_bloque_xml_empty)
        assert result["id"] == "da1"
        assert result["tipo"] == "disposicion"
        assert result["version"]["id_norma"] == "BOE-A-2014-12328"


class TestParseBloqueNoVersion:
    """Test parse_bloque when <version> element is missing."""

    def test_version_is_empty_dict(self, sample_bloque_xml_no_version):
        result = parse_bloque(sample_bloque_xml_no_version)
        assert result["version"] == {}

    def test_still_extracts_text(self, sample_bloque_xml_no_version):
        result = parse_bloque(sample_bloque_xml_no_version)
        assert "tributo de caracter directo" in result["texto_markdown"]

    def test_extracts_heading_from_articulo_class(self, sample_bloque_xml_no_version):
        result = parse_bloque(sample_bloque_xml_no_version)
        assert "## Articulo 1. Naturaleza del impuesto." in result["texto_markdown"]


class TestParseBloqueMultiClass:
    """Test parse_bloque with multiple CSS classes (parrafo, parrafo_2, parrafo_3)."""

    def test_heading_present(self, sample_bloque_xml_multi_class):
        result = parse_bloque(sample_bloque_xml_multi_class)
        assert "## Articulo 15. Gastos no deducibles." in result["texto_markdown"]

    def test_parrafo_not_indented(self, sample_bloque_xml_multi_class):
        result = parse_bloque(sample_bloque_xml_multi_class)
        lines = result["texto_markdown"].split("\n")
        parrafo_lines = [l for l in lines if l.startswith("No tendran")]
        assert len(parrafo_lines) == 1
        assert not parrafo_lines[0].startswith(" ")

    def test_parrafo_2_indented_2_spaces(self, sample_bloque_xml_multi_class):
        result = parse_bloque(sample_bloque_xml_multi_class)
        lines = result["texto_markdown"].split("\n")
        indent1_lines = [l for l in lines if "retribucion" in l]
        assert len(indent1_lines) == 1
        assert indent1_lines[0].startswith("  ")
        assert not indent1_lines[0].startswith("    ")

    def test_parrafo_3_indented_4_spaces(self, sample_bloque_xml_multi_class):
        result = parse_bloque(sample_bloque_xml_multi_class)
        lines = result["texto_markdown"].split("\n")
        indent2_lines = [l for l in lines if "multas" in l]
        assert len(indent2_lines) == 1
        assert indent2_lines[0].startswith("    ")


class TestParseBloqueEdgeCases:
    """Edge cases for parse_bloque."""

    def test_no_bloque_raises(self):
        with pytest.raises(ValueError, match="No <bloque>"):
            parse_bloque("<root><other/></root>")

    def test_invalid_xml_raises(self):
        with pytest.raises(Exception):
            parse_bloque("this is not xml at all")


# ---------------------------------------------------------------------------
# parse_indice
# ---------------------------------------------------------------------------


class TestParseIndice:
    """Test parse_indice JSON parsing."""

    def test_parses_nested_items(self, sample_indice_json):
        result = parse_indice(sample_indice_json)
        assert len(result) == 6
        assert result[0]["id"] == "tpreliminar"
        assert result[1]["id"] == "a1"

    def test_extracts_titulo(self, sample_indice_json):
        result = parse_indice(sample_indice_json)
        assert "Naturaleza" in result[0]["titulo"]

    def test_extracts_fecha(self, sample_indice_json):
        result = parse_indice(sample_indice_json)
        assert result[0]["fecha_actualizacion"] == "20240101"

    def test_empty_input(self):
        result = parse_indice({"data": {"items": []}})
        assert result == []

    def test_flat_list_input(self):
        data = [
            {"id": "a1", "titulo": "Art 1", "fecha_actualizacion": "20240101"}
        ]
        result = parse_indice(data)
        assert len(result) == 1
        assert result[0]["id"] == "a1"
