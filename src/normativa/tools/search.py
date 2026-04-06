"""Herramientas de busqueda de legislacion espanola."""

from __future__ import annotations

import logging
from typing import Any

from normativa.tools._shared import get_client
from normativa.domains import (
    DOMINIOS,
    AVAILABLE_DOMAINS,
    buscar_por_keywords,
    keywords_para_dominio,
)
from normativa.registry import search_domains, load_domain

logger = logging.getLogger(__name__)


def _simplificar_resultado(item: dict) -> dict[str, Any]:
    """Extrae campos clave de un resultado de legislacion BOE."""
    return {
        "boe_id": item.get("id", item.get("identificador", "")),
        "titulo": item.get("titulo", item.get("title", "")),
        "rango": item.get("rango", item.get("tipo", "")),
        "fecha": item.get("fecha_publicacion", item.get("fecha", "")),
        "estado": item.get("estado_consolidacion", item.get("vigencia", "")),
        "url": item.get("url_eli", item.get("url", "")),
    }


def _extraer_items(data: dict) -> list[dict]:
    """Extrae la lista de items del envelope de la API."""
    if isinstance(data, list):
        return data
    return data.get("data", data.get("items", data.get("legislacion", [])))


def _leyes_from_registry(query: str) -> list[dict[str, Any]]:
    """Search domain registries for laws matching *query* terms."""
    matches = search_domains(query)
    leyes: list[dict[str, Any]] = []
    seen: set[str] = set()
    for match in matches:
        try:
            cfg = load_domain(match["slug"])
        except Exception:
            continue
        for boe_id, ley in cfg.leyes_clave.items():
            if boe_id in seen:
                continue
            seen.add(boe_id)
            entry: dict[str, Any] = {
                "boe_id": boe_id,
                "titulo": ley.titulo_oficial,
                "nombre_corto": ley.nombre_corto,
                "rango": ley.rango,
                "dominio": match["slug"],
            }
            if ley.eu_refs:
                entry["eu_refs"] = [
                    {"celex": r.celex, "titulo": r.titulo, "tipo": r.tipo,
                     "relacion": r.relacion, "eli_url": r.eli_url}
                    for r in ley.eu_refs
                ]
            leyes.append(entry)
    return leyes


async def buscar_legislacion(
    query: str,
    rango: str = "",
    departamento: str = "",
    ambito: str = "",
    fecha_desde: str = "",
    fecha_hasta: str = "",
    limit: int = 10,
    offset: int = 0,
) -> dict[str, Any]:
    """Busca legislacion espanola en el BOE.

    Parametros principales:
    - query: texto libre de busqueda (ej: "proteccion datos personales")
    - rango: filtro por tipo de norma (Ley, Real Decreto, Orden...)
    - departamento: organismo emisor
    - fecha_desde/fecha_hasta: rango de fechas en formato YYYYMMDD
    - limit: maximo resultados (default 10, max 50)

    Devuelve lista simplificada con boe_id, titulo, rango, fecha, estado y url.
    """
    try:
        limit = min(limit, 50)
        try:
            client = await get_client()
            data = await client.legislacion_lista(
                limit=limit,
                offset=offset,
                from_date=fecha_desde or None,
                to_date=fecha_hasta or None,
                query=query or None,
            )

            items = _extraer_items(data)
            resultados = [_simplificar_resultado(item) for item in items]

            return {
                "total": data.get("total", len(resultados)),
                "offset": offset,
                "limit": limit,
                "resultados": resultados,
            }
        except Exception as api_exc:
            # BOE API failed — fall back to local domain registry
            logger.warning("BOE API search failed (%s), falling back to registry", api_exc)
            leyes = _leyes_from_registry(query)
            return {
                "total": len(leyes),
                "offset": 0,
                "limit": limit,
                "fuente": "registro_local",
                "nota": f"API BOE no disponible ({api_exc}). Resultados del registro local de dominios.",
                "resultados": leyes[:limit],
            }
    except Exception as exc:
        return {"error": str(exc), "tool": "buscar_legislacion", "resultados": []}


async def buscar_por_dominio(
    dominio: str = "",
    subtema: str = "",
    caso_uso: str = "",
) -> dict[str, Any]:
    """Busca legislacion por dominio tematico (el diferenciador clave de normativa).

    En vez de construir queries complejas, indica el dominio juridico y normativa
    selecciona automaticamente los terminos, materias y rangos adecuados.

    Dominios disponibles: laboral, fiscal, mercantil, autonomos, administrativo,
    penal, civil, proteccion_datos, digital, vivienda, medioambiental, consumo.

    Parametros:
    - dominio: clave del dominio (ej: "laboral", "fiscal"). Si vacio, busca en todos.
    - subtema: especialidad dentro del dominio (ej: "despido", "irpf")
    - caso_uso: descripcion libre del caso para refinar la busqueda

    Ejemplo: buscar_por_dominio("laboral", subtema="despido")
    """
    try:
        # When no domain specified, search across ALL domains using registry
        if not dominio:
            search_text = caso_uso or subtema or ""
            if not search_text:
                return {
                    "error": "Indica un dominio o un caso_uso/subtema para buscar.",
                    "tool": "buscar_por_dominio",
                    "dominios_disponibles": list(DOMINIOS.keys()),
                    "resultados": [],
                }
            # Cross-domain search
            domain_matches = search_domains(search_text)
            if domain_matches:
                dominio = domain_matches[0]["slug"]
            else:
                # Also try keyword matching from flat DOMINIOS
                kw_matches = buscar_por_keywords(search_text)
                if kw_matches:
                    dominio = kw_matches[0][0]
                else:
                    return {
                        "error": f"No se encontro dominio para '{search_text}'.",
                        "tool": "buscar_por_dominio",
                        "dominios_disponibles": list(DOMINIOS.keys()),
                        "resultados": [],
                    }

        dom = DOMINIOS.get(dominio)
        if dom is None:
            # Intentar encontrarlo por keywords del caso_uso
            if caso_uso:
                matches = buscar_por_keywords(caso_uso)
                if matches:
                    dominio = matches[0][0]
                    dom = matches[0][1]

            if dom is None:
                dominios_disponibles = list(DOMINIOS.keys())
                return {
                    "error": f"Dominio '{dominio}' no encontrado.",
                    "tool": "buscar_por_dominio",
                    "dominios_disponibles": dominios_disponibles,
                    "resultados": [],
                }

        # Si el dominio tiene DomainConfig rico, extraer leyes clave
        leyes_clave: list[dict[str, Any]] = []
        if dominio in AVAILABLE_DOMAINS:
            try:
                cfg = load_domain(dominio)
                for boe_id, ley in cfg.leyes_clave.items():
                    entry: dict[str, Any] = {
                        "boe_id": boe_id,
                        "nombre_corto": ley.nombre_corto,
                        "rango": ley.rango,
                    }
                    if ley.eu_refs:
                        entry["eu_refs"] = [
                            {
                                "celex": ref.celex,
                                "titulo": ref.titulo,
                                "tipo": ref.tipo,
                                "relacion": ref.relacion,
                                "eli_url": ref.eli_url,
                            }
                            for ref in ley.eu_refs
                        ]
                    leyes_clave.append(entry)
            except Exception:
                pass  # Fallback a busqueda por keywords

        # Construir query con keywords del dominio
        kws = keywords_para_dominio(dominio, subtema or None)
        if caso_uso:
            query_parts = [caso_uso] + kws[:3]
        else:
            query_parts = kws[:5]
        query_text = " ".join(query_parts)

        try:
            client = await get_client()
            data = await client.legislacion_lista(
                limit=15,
                query=query_text,
            )
            items = _extraer_items(data)
            resultados = [_simplificar_resultado(item) for item in items]
        except Exception as api_exc:
            # BOE API failed — use registry laws as fallback
            logger.warning("BOE API failed (%s), returning registry laws for domain %s", api_exc, dominio)
            resultados = []
            if leyes_clave:
                resultados = []
                for lc in leyes_clave:
                    r: dict[str, Any] = {"boe_id": lc["boe_id"], "titulo": lc["nombre_corto"], "rango": lc["rango"]}
                    if "eu_refs" in lc:
                        r["eu_refs"] = lc["eu_refs"]
                    resultados.append(r)
            resultado: dict[str, Any] = {
                "dominio": dominio,
                "nombre_dominio": dom["nombre"],
                "subtema": subtema or None,
                "query_generada": query_text,
                "fuente": "registro_local",
                "nota": f"API BOE no disponible ({api_exc}). Leyes clave del registro local.",
                "total": len(resultados),
                "resultados": resultados,
            }
            if leyes_clave:
                resultado["leyes_clave"] = leyes_clave
            return resultado

        resultado = {
            "dominio": dominio,
            "nombre_dominio": dom["nombre"],
            "subtema": subtema or None,
            "query_generada": query_text,
            "total": data.get("total", len(resultados)),
            "resultados": resultados[:15],
        }
        if leyes_clave:
            resultado["leyes_clave"] = leyes_clave

        return resultado
    except Exception as exc:
        return {"error": str(exc), "tool": "buscar_por_dominio", "resultados": []}
