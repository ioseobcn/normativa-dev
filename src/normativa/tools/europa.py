"""Herramienta de lectura de normas de la UE publicadas en el DOUE.

La API de datos abiertos del BOE no cubre el DOUE, pero el BOE sirve esos
documentos en XML por su buscador. Esto da acceso al derecho de la UE tal
como se publico (AI Act, DSA, RGPD...), en espanol y con estructura.
"""

from __future__ import annotations

import re
from typing import Any

from normativa.domains import AVAILABLE_DOMAINS
from normativa.registry import load_domain
from normativa.tools._shared import get_client, get_cache
from normativa.xml_parser import parse_doue, render_doue_segmento

_ROMANOS = "ivxlcdm"


def _normalizar_segmento(articulo: str) -> str:
    """'5', 'articulo 5' → a5; 'anexo III', 'anexo 3' → anexoiii; ids tal cual."""
    limpio = articulo.strip().lower().replace("\xa0", " ")
    m = re.match(r"^(?:art(?:iculo|ículo|\.)?\s*)?(\d+)$", limpio)
    if m:
        return f"a{m.group(1)}"
    m = re.match(r"^anexo\s*([ivxlcdm]+|\d+)$", limpio)
    if m:
        num = m.group(1)
        if num.isdigit():
            # anexos van numerados en romano en el DOUE
            valores = [(1000, "m"), (900, "cm"), (500, "d"), (400, "cd"), (100, "c"),
                       (90, "xc"), (50, "l"), (40, "xl"), (10, "x"), (9, "ix"),
                       (5, "v"), (4, "iv"), (1, "i")]
            n, romano = int(num), ""
            for valor, letra in valores:
                while n >= valor:
                    romano += letra
                    n -= valor
            num = romano
        return f"anexo{num}"
    return limpio.replace(" ", "")


def _doue_id_por_celex(celex: str) -> str | None:
    """Busca en los dominios un EURef con ese celex y doue_id conocido."""
    for name in AVAILABLE_DOMAINS:
        try:
            cfg = load_domain(name)
        except Exception:
            continue
        for ref in cfg.normas_ue:
            if ref.celex == celex and ref.doue_id:
                return ref.doue_id
        for ley in cfg.leyes_clave.values():
            for ref in ley.eu_refs:
                if ref.celex == celex and ref.doue_id:
                    return ref.doue_id
    return None


async def leer_norma_ue(doue_id: str, articulo: str = "") -> dict[str, Any]:
    """Lee una norma de la UE publicada en el DOUE (reglamentos, directivas).

    Complemento europeo de leer_indice/leer_articulo: la legislacion
    consolidada del BOE solo cubre normas espanolas; los reglamentos UE
    (AI Act, RGPD, DSA...) se publican en el DOUE. Texto en espanol tal
    como se publico (sin consolidar).

    Parametros:
    - doue_id: identificador DOUE (ej: "DOUE-L-2024-81079" para el AI Act).
      Tambien acepta un numero CELEX (ej: "32024R1689") si esta mapeado en
      los dominios tematicos.
    - articulo: opcional. Numero de articulo ("5", "articulo 5"), anexo
      ("anexo III") o "preambulo". Si se omite, devuelve metadatos + indice
      de articulos para elegir cual leer sin cargar la norma entera.

    Devuelve: sin articulo → metadatos, materias, notas e indice; con
    articulo → el texto de ese articulo/anexo en Markdown.
    """
    try:
        doue_id = doue_id.strip()
        if not doue_id:
            return {"error": "doue_id es obligatorio.", "tool": "leer_norma_ue"}

        if not doue_id.startswith("DOUE-"):
            mapeado = _doue_id_por_celex(doue_id)
            if mapeado is None:
                return {
                    "error": (
                        f"'{doue_id}' no es un id DOUE ni un CELEX mapeado. "
                        "Usa el formato DOUE-L-YYYY-NNNNN."
                    ),
                    "tool": "leer_norma_ue",
                }
            doue_id = mapeado

        client = await get_client()
        cache = await get_cache()
        xml_text = await cache.get_or_fetch(
            "doue", doue_id, lambda: client.doue_documento(doue_id)
        )

        parsed = parse_doue(xml_text)
        segmentos = parsed["segmentos"]

        if not articulo:
            return {
                "doue_id": doue_id,
                "metadatos": parsed["metadatos"],
                "materias": parsed["analisis"].get("materias", []),
                "notas": parsed["analisis"].get("notas", []),
                "total_segmentos": len(segmentos),
                "indice": [{"id": s["id"], "titulo": s["titulo"]} for s in segmentos],
            }

        seg_id = _normalizar_segmento(articulo)
        seg = next((s for s in segmentos if s["id"] == seg_id), None)
        if seg is None:
            return {
                "error": f"Segmento '{articulo}' no encontrado en {doue_id}.",
                "tool": "leer_norma_ue",
                "doue_id": doue_id,
                "segmentos_disponibles": [s["id"] for s in segmentos][:40],
            }

        return {
            "doue_id": doue_id,
            "segmento": seg["id"],
            "titulo": seg["titulo"],
            "norma": parsed["metadatos"].get("titulo", ""),
            "nota_vigencia": "; ".join(parsed["analisis"].get("notas", [])) or None,
            "texto": render_doue_segmento(seg),
        }
    except Exception as exc:
        return {"error": str(exc), "tool": "leer_norma_ue", "doue_id": doue_id}
