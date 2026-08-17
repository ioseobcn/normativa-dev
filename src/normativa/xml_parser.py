"""Parse BOE XML text blocks into clean Markdown."""

from __future__ import annotations

from datetime import date
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


def _version_meta(elem: ET.Element) -> dict[str, str]:  # type: ignore[name-defined]
    return {
        "id_norma": elem.get("id_norma", ""),
        "fecha_publicacion": elem.get("fecha_publicacion", ""),
        "fecha_vigencia": elem.get("fecha_vigencia", ""),
    }


def _render_markdown(source: ET.Element) -> str:  # type: ignore[name-defined]
    """Convert the <p> children of *source* into Markdown text."""
    paragraphs: list[str] = []
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

    return "\n".join(md_lines).strip()


def parse_bloque(xml_text: str, fecha_vigencia: str | None = None) -> dict[str, Any]:
    """Parse a BOE ``texto/bloque`` XML response into a structured dict.

    A block carries one ``<version>`` element per consolidation (original
    text plus each amendment), oldest first. By default the text returned is
    the version in force today (latest ``fecha_vigencia`` not in the future);
    pass *fecha_vigencia* (YYYYMMDD) to select a specific historic version.

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
            "versiones": [ ...metadata de todas las versiones... ],
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

    versiones = bloque.findall("version")

    selected: ET.Element | None = None  # type: ignore[name-defined]
    if versiones:
        if fecha_vigencia:
            for v in versiones:
                if v.get("fecha_vigencia", "") == fecha_vigencia:
                    selected = v
                    break
            if selected is None:
                raise ValueError(
                    f"No hay version con fecha_vigencia={fecha_vigencia}. "
                    f"Disponibles: {[v.get('fecha_vigencia', '') for v in versiones]}"
                )
        else:
            # Version vigente hoy: la ultima cuya vigencia no sea futura.
            hoy = date.today().strftime("%Y%m%d")
            vigentes = [v for v in versiones if v.get("fecha_vigencia", "") <= hoy]
            selected = vigentes[-1] if vigentes else versiones[0]

    source = selected if selected is not None else bloque
    texto_markdown = _render_markdown(source)

    return {
        "id": bloque_id,
        "tipo": tipo,
        "titulo": titulo,
        "version": _version_meta(selected) if selected is not None else {},
        "versiones": [_version_meta(v) for v in versiones],
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
        items = items.get("bloque", items.get("items", items.get("contenido", [items])))

    # Real API shape: data is [{"bloque": [{id, titulo, ...}, ...]}] —
    # flatten the "bloque" wrappers into a single list.
    if (
        isinstance(items, list)
        and items
        and isinstance(items[0], dict)
        and "bloque" in items[0]
    ):
        flat: list[Any] = []
        for wrapper in items:
            bloques = wrapper.get("bloque", [])
            if isinstance(bloques, list):
                flat.extend(bloques)
            elif isinstance(bloques, dict):
                flat.append(bloques)
        items = flat

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
