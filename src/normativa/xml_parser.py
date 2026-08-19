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


# -- DOUE (derecho de la UE publicado en el Diario Oficial) ----------------
#
# El BOE sirve los documentos DOUE en /buscar/xml.php con las mismas clases
# CSS que la legislacion consolidada: articulo (encabezado "Artículo N"),
# parrafo, capitulo_num/tit, seccion, anexo_num/tit, cita. El titulo del
# articulo va en el <p class="parrafo"> inmediatamente posterior.

_DOUE_META_KEYS = (
    "identificador", "titulo", "rango", "numero_oficial", "departamento",
    "fecha_disposicion", "fecha_publicacion", "fecha_vigencia", "diario",
    "url_pdf", "url_eli", "estatus_derogacion", "fecha_derogacion",
)


def _doue_walk(elem: ET.Element) -> list[tuple[str, ET.Element]]:  # type: ignore[name-defined]
    """Flatten <texto> into (kind, elem) items in document order.

    Tables are kept whole (not descended into) so their inner <p> don't
    duplicate as loose paragraphs.
    """
    items: list[tuple[str, ET.Element]] = []  # type: ignore[name-defined]
    for child in elem:
        if child.tag == "table":
            items.append(("table", child))
        elif child.tag == "p":
            items.append(("p", child))
        else:
            items.extend(_doue_walk(child))
    return items


def _doue_segment_id(clase: str, texto: str) -> str | None:
    """Id de segmento para encabezados: 'Artículo 5' → a5, 'ANEXO III' → anexoiii."""
    limpio = texto.replace("\xa0", " ").strip()
    if clase == "articulo":
        num = "".join(c for c in limpio if c.isdigit())
        if num:
            return f"a{num}"
    if clase == "anexo_num":
        resto = limpio.lower().replace("anexo", "").strip()
        return f"anexo{resto}" if resto else "anexo"
    return None


def _table_to_markdown(table: ET.Element) -> str:  # type: ignore[name-defined]
    filas: list[str] = []
    for tr in table.iter("tr"):
        celdas = ["".join(td.itertext()).replace("\xa0", " ").strip() for td in tr if td.tag == "td"]
        if any(celdas):
            filas.append("| " + " | ".join(celdas) + " |")
    return "\n".join(filas)


def parse_doue(xml_text: str) -> dict[str, Any]:
    """Parse a BOE DOUE document into metadata, analysis, and text segments.

    Returns metadatos (subset), analisis (materias, notas), and segmentos:
    a list of {id, titulo, elems} where elems are the (kind, elem) items of
    that article/annex, ready for render_doue_segmento().
    """
    root = ET.fromstring(xml_text)
    if root.tag != "documento":
        raise ValueError("XML DOUE sin raiz <documento>")

    meta_elem = root.find("metadatos")
    metadatos = {
        k: (meta_elem.findtext(k) or "").strip()
        for k in _DOUE_META_KEYS
        if meta_elem is not None
    }

    analisis: dict[str, Any] = {}
    an = root.find("analisis")
    if an is not None:
        analisis["materias"] = [
            (m.text or "").strip() for m in an.iter("materia") if (m.text or "").strip()
        ]
        analisis["notas"] = [
            (n.text or "").strip() for n in an.iter("nota") if (n.text or "").strip()
        ]

    texto = root.find("texto")
    items = _doue_walk(texto) if texto is not None else []

    # Segmentar por encabezados de articulo/anexo. Lo anterior al primer
    # encabezado (exposicion de motivos, considerandos) va a "preambulo".
    segmentos: list[dict[str, Any]] = [{"id": "preambulo", "titulo": "Preámbulo y considerandos", "elems": []}]
    for kind, elem in items:
        clase = elem.get("class", "") if kind == "p" else ""
        seg_id = _doue_segment_id(clase, "".join(elem.itertext())) if kind == "p" else None
        if seg_id:
            titulo_visible = "".join(elem.itertext()).replace("\xa0", " ").strip()
            segmentos.append({"id": seg_id, "titulo": titulo_visible, "elems": [(kind, elem)]})
        else:
            segmentos[-1]["elems"].append((kind, elem))

    # El titulo real del articulo es el primer parrafo corto tras el encabezado
    for seg in segmentos[1:]:
        for kind, elem in seg["elems"][1:3]:
            if kind != "p":
                break
            txt = "".join(elem.itertext()).replace("\xa0", " ").strip()
            clase = elem.get("class", "")
            if clase in ("parrafo", "anexo_tit") and txt and len(txt) < 150 and not txt[0].isdigit():
                seg["titulo"] = f"{seg['titulo']}. {txt}"
                break

    return {"metadatos": metadatos, "analisis": analisis, "segmentos": segmentos}


def render_doue_segmento(segmento: dict[str, Any]) -> str:
    """Render one parse_doue() segment as Markdown."""
    lineas: list[str] = []
    for kind, elem in segmento["elems"]:
        if kind == "table":
            md = _table_to_markdown(elem)
            if md:
                lineas.append(md)
            continue
        clase = elem.get("class", "")
        txt = "".join(elem.itertext()).replace("\xa0", " ").strip()
        if not txt:
            continue
        if clase in ("articulo", "anexo_num", "capitulo_num", "seccion"):
            lineas.append(f"## {txt}")
        elif clase in ("anexo_tit", "capitulo_tit"):
            lineas.append(f"### {txt}")
        else:
            lineas.append(txt)
    return "\n\n".join(lineas).strip()


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
