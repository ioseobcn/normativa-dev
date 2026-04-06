"""Parse BOE XML text blocks into clean Markdown."""

from __future__ import annotations

from typing import Any

import defusedxml.ElementTree as ET


# -- CSS class to Markdown mapping ----------------------------------------

_CLASS_MAP: dict[str, str] = {
    "articulo": "heading",
    "parrafo": "paragraph",
    "parrafo_2": "indent_1",
    "parrafo_3": "indent_2",
}


def _element_text(elem: ET.Element) -> str:  # type: ignore[name-defined]
    """Extract all text from an element, including tail of children."""
    return "".join(elem.itertext()).strip()


def _p_to_markdown(p: ET.Element) -> str:  # type: ignore[name-defined]
    """Convert a single <p> element to a Markdown line."""
    css_class = p.get("class", "")
    text = _element_text(p)
    if not text:
        return ""

    kind = _CLASS_MAP.get(css_class, "paragraph")

    if kind == "heading":
        return f"## {text}"
    if kind == "indent_1":
        return f"  {text}"
    if kind == "indent_2":
        return f"    {text}"
    # paragraph / unknown
    return text


# -- Public API -----------------------------------------------------------


def parse_bloque(xml_text: str) -> dict[str, Any]:
    """Parse a BOE ``texto/bloque`` XML response into a structured dict.

    Returns::

        {
            "id": "a1",
            "tipo": "precepto",
            "titulo": "Articulo 1.",
            "version": {
                "id_norma": "BOE-A-2006-20764",
                "fecha_publicacion": "20061129",
                "fecha_vigencia": "20070101",
            },
            "texto_markdown": "## Articulo 1. Naturaleza ...\\n\\nEl Impuesto...",
        }
    """
    root = ET.fromstring(xml_text)

    # Navigate the response envelope: <response><data><bloque>
    bloque = root.find(".//bloque")
    if bloque is None:
        # Maybe the XML *is* the <bloque> directly (no envelope).
        if root.tag == "bloque":
            bloque = root
        else:
            raise ValueError("No <bloque> element found in XML")

    bloque_id: str = bloque.get("id", "")
    tipo: str = bloque.get("tipo", "")
    titulo: str = bloque.get("titulo", "")

    # Version info
    version_elem = bloque.find("version")
    version_info: dict[str, str] = {}
    if version_elem is not None:
        version_info = {
            "id_norma": version_elem.get("id_norma", ""),
            "fecha_publicacion": version_elem.get("fecha_publicacion", ""),
            "fecha_vigencia": version_elem.get("fecha_vigencia", ""),
        }

    # Convert <p> elements to Markdown lines
    paragraphs: list[str] = []
    source = version_elem if version_elem is not None else bloque
    for p in source.findall("p"):
        line = _p_to_markdown(p)
        if line:
            paragraphs.append(line)

    # Join with blank lines between paragraphs; headings get an extra blank after.
    md_lines: list[str] = []
    for line in paragraphs:
        if line.startswith("## "):
            if md_lines:
                md_lines.append("")
            md_lines.append(line)
            md_lines.append("")
        else:
            md_lines.append(line)

    texto_markdown = "\n".join(md_lines).strip()

    return {
        "id": bloque_id,
        "tipo": tipo,
        "titulo": titulo,
        "version": version_info,
        "texto_markdown": texto_markdown,
    }


def parse_indice(data: dict) -> list[dict[str, str]]:
    """Parse an ``indice`` JSON response into a flat list.

    Each item has keys: ``id``, ``titulo``, ``fecha_actualizacion``.

    The API may nest the list under ``data``, ``items``, or return it directly.
    """
    # Unwrap envelope
    items: Any = data
    if isinstance(data, dict):
        items = data.get("data", data.get("items", []))

    if isinstance(items, dict):
        # Some responses nest further
        items = items.get("items", items.get("contenido", [items]))

    result: list[dict[str, str]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        result.append(
            {
                "id": item.get("id", item.get("bloque_id", "")),
                "titulo": item.get("titulo", item.get("title", "")),
                "fecha_actualizacion": item.get(
                    "fecha_actualizacion",
                    item.get("fecha_vigencia", item.get("updated", "")),
                ),
            }
        )

    return result
