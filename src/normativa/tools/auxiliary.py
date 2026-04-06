"""Herramienta de datos auxiliares de referencia del BOE."""

from __future__ import annotations

from typing import Any

from normativa.tools._shared import get_client, get_cache


async def datos_auxiliares(
    tipo: str,
    buscar: str = "",
) -> dict[str, Any]:
    """Consulta datos auxiliares de referencia del BOE.

    Tipos disponibles:
    - materias: lista de materias/temas juridicos del BOE
    - departamentos: organismos emisores (ministerios, tribunales, etc.)
    - rangos: tipos de norma (Ley, Real Decreto, Orden, etc.)
    - ambitos: ambitos territoriales (estatal, autonomico, etc.)

    Parametros:
    - tipo: uno de materias, departamentos, rangos, ambitos
    - buscar: texto para filtrar resultados (opcional)

    Devuelve: lista de valores del tipo solicitado.
    """
    try:
        tipos_validos = {"materias", "departamentos", "rangos", "ambitos"}
        if tipo not in tipos_validos:
            return {
                "error": f"Tipo '{tipo}' no valido. Usa: {', '.join(sorted(tipos_validos))}",
                "tool": "datos_auxiliares",
            }

        client = await get_client()
        cache = await get_cache()
        data = await cache.get_or_fetch(
            "auxiliares", tipo, lambda: client.datos_auxiliares(tipo)
        )

        # Extraer lista del envelope
        if isinstance(data, dict):
            items = data.get("data", data.get("items", data.get(tipo, [])))
        elif isinstance(data, list):
            items = data
        else:
            items = []

        # Filtrar por texto si se proporciona
        if buscar and isinstance(items, list):
            buscar_l = buscar.lower()
            items_filtrados = []
            for item in items:
                texto_item = ""
                if isinstance(item, str):
                    texto_item = item
                elif isinstance(item, dict):
                    texto_item = " ".join(str(v) for v in item.values())
                if buscar_l in texto_item.lower():
                    items_filtrados.append(item)
            items = items_filtrados

        # Limitar para no saturar contexto
        total = len(items) if isinstance(items, list) else 0
        if isinstance(items, list) and len(items) > 100:
            items = items[:100]
            truncado = True
        else:
            truncado = False

        return {
            "tipo": tipo,
            "buscar": buscar or None,
            "total": total,
            "truncado": truncado,
            "items": items,
        }
    except Exception as exc:
        return {"error": str(exc), "tool": "datos_auxiliares", "tipo": tipo}
