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


def _as_list(value: Any) -> list:
    """La conversion XML->JSON del BOE devuelve dict con un elemento y lista con varios."""
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _url_pdf(item: dict) -> str:
    """url_pdf viene como {"szBytes": ..., "texto": "https://..."} o string."""
    url = item.get("url_pdf", "")
    if isinstance(url, dict):
        return url.get("texto", "")
    return url


def _extraer_entradas_sumario(data: dict) -> list[dict[str, Any]]:
    """Aplana el sumario real: data.sumario.diario[].seccion[].departamento[].[epigrafe[]].item[].

    Cada entrada sale ya simplificada con el contexto (seccion, departamento,
    epigrafe) de la rama donde estaba anidada. Los items pueden colgar del
    departamento directamente (seccion V) o de la seccion (BORME).
    """
    entradas: list[dict[str, Any]] = []

    def emitir(item: Any, seccion: str, departamento: str, epigrafe: str) -> None:
        if not isinstance(item, dict):
            return
        entradas.append({
            "boe_id": item.get("identificador", item.get("id", "")),
            "titulo": item.get("titulo", ""),
            "seccion": seccion,
            "departamento": departamento,
            "epigrafe": epigrafe,
            "url_pdf": _url_pdf(item),
            "url_html": item.get("url_html", ""),
        })

    sumario = data.get("data", {}).get("sumario", {}) if isinstance(data, dict) else {}
    for diario in _as_list(sumario.get("diario")):
        if not isinstance(diario, dict):
            continue
        for seccion in _as_list(diario.get("seccion")):
            if not isinstance(seccion, dict):
                continue
            nombre_seccion = f"{seccion.get('codigo', '')} {seccion.get('nombre', '')}".strip()
            # BORME: items directamente bajo la seccion
            for item in _as_list(seccion.get("item")):
                emitir(item, nombre_seccion, "", "")
            for dep in _as_list(seccion.get("departamento")):
                if not isinstance(dep, dict):
                    continue
                nombre_dep = dep.get("nombre", "")
                # Seccion V: items directamente bajo el departamento
                for item in _as_list(dep.get("item")):
                    emitir(item, nombre_seccion, nombre_dep, "")
                for epigrafe in _as_list(dep.get("epigrafe")):
                    if not isinstance(epigrafe, dict):
                        continue
                    for item in _as_list(epigrafe.get("item")):
                        emitir(item, nombre_seccion, nombre_dep, epigrafe.get("nombre", ""))

    return entradas


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

        resultados = _extraer_entradas_sumario(data)

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

        resultados = _extraer_entradas_sumario(data)

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
