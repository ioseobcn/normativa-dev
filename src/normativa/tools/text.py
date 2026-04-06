"""Herramientas de lectura de textos legales — las mas criticas para eficiencia de contexto.

Patron de uso recomendado por el LLM:
1. leer_indice() para ver la estructura de la norma
2. leer_articulo() para leer UN articulo concreto
3. leer_articulos_rango() solo si necesita un bloque consecutivo
"""

from __future__ import annotations

from typing import Any

from normativa.boe_client import BOEClient
from normativa.tools._shared import get_client, get_cache
from normativa.xml_parser import parse_bloque, parse_indice


async def leer_indice(boe_id: str) -> dict[str, Any]:
    """Lee el indice (tabla de contenidos) de una norma consolidada.

    Devuelve la lista de bloques/articulos con su id y titulo, para que
    puedas elegir cual leer sin cargar el texto completo.

    Parametros:
    - boe_id: identificador BOE (ej: "BOE-A-2006-20764")

    Devuelve: lista de {id, titulo} — usa el id para leer_articulo().
    """
    try:
        if not boe_id or not boe_id.startswith("BOE"):
            return {"error": f"boe_id invalido: '{boe_id}'. Debe empezar por 'BOE-'.", "tool": "leer_indice"}

        client = await get_client()
        cache = await get_cache()
        data = await cache.get_or_fetch(
            "indices", boe_id, lambda: client.legislacion_indice(boe_id)
        )

        # data ya es list[dict] gracias a BOEClient.legislacion_indice
        if isinstance(data, list):
            items = parse_indice({"items": data})
        elif isinstance(data, dict):
            items = parse_indice(data)
        else:
            items = []

        # Simplificar para contexto minimo
        indice = [{"id": it["id"], "titulo": it["titulo"]} for it in items if it.get("id")]

        return {
            "boe_id": boe_id,
            "total_bloques": len(indice),
            "indice": indice,
        }
    except Exception as exc:
        return {"error": str(exc), "tool": "leer_indice", "boe_id": boe_id}


async def leer_articulo(boe_id: str, bloque_id: str) -> dict[str, Any]:
    """Lee UN articulo/bloque concreto de una norma, devuelto como Markdown.

    Esta es la herramienta principal para leer legislacion: pide exactamente
    el articulo que necesitas en vez de cargar toda la ley.

    Parametros:
    - boe_id: identificador BOE (ej: "BOE-A-2006-20764")
    - bloque_id: id del bloque (ej: "a1", "a25") — obtenlo de leer_indice()

    Devuelve: texto del articulo en Markdown limpio.
    """
    try:
        if not boe_id or not boe_id.startswith("BOE"):
            return {"error": f"boe_id invalido: '{boe_id}'. Debe empezar por 'BOE-'.", "tool": "leer_articulo"}
        if not bloque_id:
            return {"error": "bloque_id es obligatorio. Usa leer_indice() para ver los ids.", "tool": "leer_articulo"}

        client = await get_client()
        cache = await get_cache()
        xml_text = await cache.get_or_fetch(
            "bloques", (boe_id, bloque_id),
            lambda: client.legislacion_bloque(boe_id, bloque_id),
        )

        parsed = parse_bloque(xml_text)

        return {
            "boe_id": boe_id,
            "bloque_id": parsed.get("id", bloque_id),
            "titulo": parsed.get("titulo", ""),
            "tipo": parsed.get("tipo", ""),
            "version": parsed.get("version", {}),
            "texto": parsed.get("texto_markdown", ""),
        }
    except Exception as exc:
        return {"error": str(exc), "tool": "leer_articulo", "boe_id": boe_id, "bloque_id": bloque_id}


async def leer_articulos_rango(
    boe_id: str,
    desde: str,
    hasta: str,
    max_bloques: int = 10,
) -> dict[str, Any]:
    """Lee un rango consecutivo de articulos de una norma.

    Util cuando necesitas varios articulos seguidos (ej: del a1 al a5).
    Limitado a max_bloques para no saturar el contexto.

    Parametros:
    - boe_id: identificador BOE
    - desde: id del primer bloque (ej: "a1")
    - hasta: id del ultimo bloque (ej: "a5")
    - max_bloques: maximo de bloques a leer (default 10)

    Devuelve: lista de articulos con su texto en Markdown.
    """
    try:
        if not boe_id or not boe_id.startswith("BOE"):
            return {"error": f"boe_id invalido: '{boe_id}'. Debe empezar por 'BOE-'.", "tool": "leer_articulos_rango"}
        if not desde or not hasta:
            return {"error": "desde y hasta son obligatorios.", "tool": "leer_articulos_rango"}

        max_bloques = min(max_bloques, 20)  # Hard cap

        client = await get_client()
        cache = await get_cache()

        # Primero obtener el indice para saber que bloques hay en el rango
        idx_data = await cache.get_or_fetch(
            "indices", boe_id, lambda: client.legislacion_indice(boe_id)
        )

        if isinstance(idx_data, list):
            items = parse_indice({"items": idx_data})
        elif isinstance(idx_data, dict):
            items = parse_indice(idx_data)
        else:
            items = []

        # Encontrar los bloques en el rango
        ids = [it["id"] for it in items if it.get("id")]
        try:
            idx_desde = ids.index(desde)
            idx_hasta = ids.index(hasta)
        except ValueError:
            return {
                "error": f"No se encontraron los bloques '{desde}' y/o '{hasta}' en el indice.",
                "tool": "leer_articulos_rango",
                "bloques_disponibles": ids[:30],
                "boe_id": boe_id,
            }

        if idx_desde > idx_hasta:
            idx_desde, idx_hasta = idx_hasta, idx_desde

        bloques_a_leer = ids[idx_desde : idx_hasta + 1]
        if len(bloques_a_leer) > max_bloques:
            truncado = True
            bloques_a_leer = bloques_a_leer[:max_bloques]
        else:
            truncado = False

        # Leer cada bloque
        articulos = []
        for bloque_id in bloques_a_leer:
            try:
                xml_text = await cache.get_or_fetch(
                    "bloques", (boe_id, bloque_id),
                    lambda bid=bloque_id: client.legislacion_bloque(boe_id, bid),
                )
                parsed = parse_bloque(xml_text)
                articulos.append({
                    "bloque_id": parsed.get("id", bloque_id),
                    "titulo": parsed.get("titulo", ""),
                    "texto": parsed.get("texto_markdown", ""),
                })
            except Exception as exc:
                articulos.append({
                    "bloque_id": bloque_id,
                    "error": str(exc),
                })

        return {
            "boe_id": boe_id,
            "desde": desde,
            "hasta": hasta,
            "total_leidos": len(articulos),
            "truncado": truncado,
            "articulos": articulos,
        }
    except Exception as exc:
        return {"error": str(exc), "tool": "leer_articulos_rango", "boe_id": boe_id}
