"""Herramientas de metadatos y analisis de disposiciones BOE."""

from __future__ import annotations

from typing import Any

from normativa.tools._shared import get_client, get_cache


def _as_list(value: Any) -> list:
    """La conversion XML->JSON del BOE devuelve dict con un elemento y lista con varios."""
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _parse_referencias(refs_wrapper: Any, inner_key: str) -> list[dict[str, Any]]:
    """Aplana referencias.anteriores/posteriores[*].{anterior|posterior}[*]."""
    resultado: list[dict[str, Any]] = []
    for wrapper in _as_list(refs_wrapper):
        if not isinstance(wrapper, dict):
            continue
        for ref in _as_list(wrapper.get(inner_key)):
            if not isinstance(ref, dict):
                continue
            relacion = ref.get("relacion", {})
            resultado.append({
                "id_norma": ref.get("id_norma", ""),
                "relacion": relacion.get("texto", "") if isinstance(relacion, dict) else str(relacion),
                "texto": ref.get("texto", ""),
            })
    return resultado


async def obtener_metadatos(boe_id: str) -> dict[str, Any]:
    """Obtiene los metadatos completos de una disposicion del BOE.

    Parametros:
    - boe_id: identificador BOE (ej: "BOE-A-2006-20764")

    Devuelve: titulo, rango, fecha_publicacion, departamento, estado de
    consolidacion, materias, url ELI, y otros metadatos disponibles.
    """
    try:
        if not boe_id or not boe_id.startswith("BOE"):
            return {"error": f"boe_id invalido: '{boe_id}'. Debe empezar por 'BOE-'.", "tool": "obtener_metadatos"}

        client = await get_client()
        cache = await get_cache()
        data = await cache.get_or_fetch(
            "metadatos", boe_id, lambda: client.legislacion_metadatos(boe_id)
        )

        # Aplanar: la API devuelve {"status":..., "data": [item]} o {"status":..., "data": {...}}
        raw = data.get("data", data) if isinstance(data, dict) else data
        # Si es lista, tomar el primer elemento
        if isinstance(raw, list):
            meta = raw[0] if raw else {}
        else:
            meta = raw

        return {"boe_id": boe_id, "data": meta} if isinstance(meta, dict) else {"boe_id": boe_id, "raw": meta}

    except Exception as exc:
        return {"error": str(exc), "tool": "obtener_metadatos", "boe_id": boe_id}


async def obtener_analisis(
    boe_id: str,
    incluir_referencias: bool = True,
    max_referencias: int = 20,
) -> dict[str, Any]:
    """Obtiene el analisis juridico de una disposicion: materias y referencias cruzadas.

    Parametros:
    - boe_id: identificador BOE (ej: "BOE-A-2006-20764")
    - incluir_referencias: si incluir normas que afecta/es afectada por (default True)
    - max_referencias: limite de referencias por tipo (default 20)

    Devuelve: materias y referencias cruzadas — afecta_a (normas anteriores
    sobre las que actua: DEROGA, MODIFICA...) y afectada_por (normas
    posteriores que la modifican), con id_norma, relacion y descripcion.
    """
    try:
        if not boe_id or not boe_id.startswith("BOE"):
            return {"error": f"boe_id invalido: '{boe_id}'. Debe empezar por 'BOE-'.", "tool": "obtener_analisis"}

        client = await get_client()
        cache = await get_cache()
        data = await cache.get_or_fetch(
            "analisis", boe_id, lambda: client.legislacion_analisis(boe_id)
        )

        # Envelope real: {"status": ..., "data": [{materias, referencias, notas}]}
        analisis = data.get("data", data) if isinstance(data, dict) else data
        entries = _as_list(analisis)
        analisis = entries[0] if entries and isinstance(entries[0], dict) else {}

        resultado: dict[str, Any] = {"boe_id": boe_id}

        materias = [
            {"codigo": m["materia"].get("codigo", ""), "texto": m["materia"].get("texto", "")}
            for m in _as_list(analisis.get("materias"))
            if isinstance(m, dict) and isinstance(m.get("materia"), dict)
        ]
        if materias:
            resultado["materias"] = materias

        if "notas" in analisis:
            resultado["notas"] = analisis["notas"]

        if incluir_referencias:
            referencias = analisis.get("referencias", {})
            if isinstance(referencias, dict):
                # anteriores = normas previas sobre las que esta actua;
                # posteriores = normas posteriores que actuan sobre esta.
                for clave_salida, clave_api, inner in (
                    ("afecta_a", "anteriores", "anterior"),
                    ("afectada_por", "posteriores", "posterior"),
                ):
                    refs = _parse_referencias(referencias.get(clave_api), inner)
                    if refs:
                        resultado[clave_salida] = refs[:max_referencias]
                        if len(refs) > max_referencias:
                            resultado[f"{clave_salida}_total"] = len(refs)
                            resultado[f"{clave_salida}_truncado"] = True

        return resultado

    except Exception as exc:
        return {"error": str(exc), "tool": "obtener_analisis", "boe_id": boe_id}
