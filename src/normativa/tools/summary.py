"""Herramientas de sumarios diarios BOE y BORME."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from normativa.tools._shared import get_client
from normativa.domains import buscar_por_keywords


def _fecha_a_yyyymmdd(fecha: str) -> str:
    """Convierte fecha flexible a YYYYMMDD para la API."""
    if not fecha:
        return date.today().strftime("%Y%m%d")

    fecha = fecha.strip()

    # Ya es YYYYMMDD
    if len(fecha) == 8 and fecha.isdigit():
        return fecha

    # YYYY-MM-DD
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(fecha, fmt).strftime("%Y%m%d")
        except ValueError:
            continue

    return fecha  # Devolver tal cual y dejar que la API falle con mensaje claro


def _simplificar_entrada_sumario(item: dict) -> dict[str, Any]:
    """Extrae campos clave de una entrada del sumario."""
    return {
        "boe_id": item.get("id", item.get("identificador", "")),
        "titulo": item.get("titulo", item.get("title", "")),
        "seccion": item.get("seccion", ""),
        "departamento": item.get("departamento", ""),
        "rango": item.get("rango", item.get("tipo", "")),
        "url_pdf": item.get("url_pdf", item.get("url", "")),
    }


def _extraer_entradas_sumario(data: dict) -> list[dict]:
    """Extrae entradas del envelope de sumario."""
    if isinstance(data, list):
        return data
    items = data.get("data", data.get("items", data.get("sumario", [])))
    if isinstance(items, dict):
        # A veces el sumario tiene secciones anidadas
        entries = []
        for section in items.values():
            if isinstance(section, list):
                entries.extend(section)
            elif isinstance(section, dict) and "items" in section:
                entries.extend(section["items"])
        return entries if entries else [items]
    return items if isinstance(items, list) else []


async def sumario_boe(
    fecha: str = "",
    seccion: str = "",
    departamento: str = "",
    dominio: str = "",
) -> dict[str, Any]:
    """Consulta el sumario diario del BOE para una fecha dada.

    Muestra las disposiciones publicadas ese dia. Filtrable por seccion,
    departamento o dominio tematico.

    Parametros:
    - fecha: fecha del sumario (YYYY-MM-DD, DD/MM/YYYY o YYYYMMDD). Default: hoy.
    - seccion: filtrar por seccion del BOE (I, II, III, IV, V)
    - departamento: filtrar por departamento emisor
    - dominio: filtrar por dominio tematico (laboral, fiscal, etc.)

    Devuelve: lista de disposiciones publicadas.
    """
    try:
        fecha_api = _fecha_a_yyyymmdd(fecha)

        client = await get_client()
        data = await client.sumario_boe(fecha_api)

        entradas = _extraer_entradas_sumario(data)
        resultados = [_simplificar_entrada_sumario(e) for e in entradas]

        # Filtros opcionales
        if seccion:
            seccion_l = seccion.lower()
            resultados = [r for r in resultados if seccion_l in r.get("seccion", "").lower()]

        if departamento:
            dep_l = departamento.lower()
            resultados = [r for r in resultados if dep_l in r.get("departamento", "").lower()]

        if dominio:
            # Filtrar por keywords del dominio
            matches = buscar_por_keywords(dominio)
            if matches:
                kws = [kw.lower() for kw in matches[0][1]["keywords"][:8]]
                filtrados = []
                for r in resultados:
                    titulo_l = r.get("titulo", "").lower()
                    if any(kw in titulo_l for kw in kws):
                        filtrados.append(r)
                resultados = filtrados

        # Limitar output
        total = len(resultados)
        resultados = resultados[:50]

        return {
            "fecha": fecha_api,
            "total": total,
            "mostrados": len(resultados),
            "filtros": {
                "seccion": seccion or None,
                "departamento": departamento or None,
                "dominio": dominio or None,
            },
            "entradas": resultados,
        }
    except Exception as exc:
        return {"error": str(exc), "tool": "sumario_boe", "fecha": fecha}


async def sumario_borme(fecha: str = "") -> dict[str, Any]:
    """Consulta el sumario diario del BORME (Boletin Oficial del Registro Mercantil).

    Parametros:
    - fecha: fecha del sumario (YYYY-MM-DD, DD/MM/YYYY o YYYYMMDD). Default: hoy.

    Devuelve: lista de actos mercantiles publicados (constituciones, nombramientos, etc.).
    """
    try:
        fecha_api = _fecha_a_yyyymmdd(fecha)

        client = await get_client()
        data = await client.sumario_borme(fecha_api)

        entradas = _extraer_entradas_sumario(data)
        resultados = [_simplificar_entrada_sumario(e) for e in entradas]

        total = len(resultados)
        resultados = resultados[:50]

        return {
            "fecha": fecha_api,
            "total": total,
            "mostrados": len(resultados),
            "entradas": resultados,
        }
    except Exception as exc:
        return {"error": str(exc), "tool": "sumario_borme", "fecha": fecha}
