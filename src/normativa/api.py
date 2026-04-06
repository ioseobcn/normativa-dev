"""HTTP REST API para normativa — acceso a legislacion espanola via HTTP/JSON.

Usa FastAPI para generar automaticamente la especificacion OpenAPI,
compatible con ChatGPT Actions, Codex, Claude.ai web y cualquier cliente HTTP.
"""

from __future__ import annotations

from fastapi import FastAPI, Query, Path, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse

from normativa import __version__

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(
    title="normativa",
    description=(
        "API REST de legislacion espanola consolidada con dominios tematicos. "
        "Accede al BOE (Boletin Oficial del Estado), busca por dominio juridico, "
        "lee articulos individuales y consulta sumarios diarios."
    ),
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/api/openapi.json",
)

# CORS — abierto para desarrollo, configurable para produccion
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _handle_error(result: dict) -> dict:
    """Si el resultado contiene un error, lanza HTTPException."""
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


# ---------------------------------------------------------------------------
# Landing
# ---------------------------------------------------------------------------

@app.get(
    "/",
    response_class=HTMLResponse,
    summary="Pagina de inicio y health check",
    tags=["general"],
)
async def landing():
    """Pagina de inicio con enlaces a la documentacion y al spec OpenAPI."""
    return f"""<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>normativa v{__version__}</title>
<style>
body {{ font-family: system-ui, sans-serif; max-width: 640px; margin: 4rem auto; padding: 0 1rem; color: #1a1a1a; }}
h1 {{ color: #3949ab; }} a {{ color: #3949ab; }} code {{ background: #f5f5f5; padding: 2px 6px; border-radius: 3px; }}
ul {{ line-height: 2; }}
</style></head>
<body>
<h1>normativa v{__version__}</h1>
<p>API REST de legislacion espanola consolidada con dominios tematicos.</p>
<ul>
  <li><a href="/docs">Documentacion interactiva (Swagger UI)</a></li>
  <li><a href="/redoc">Documentacion (ReDoc)</a></li>
  <li><a href="/api/openapi.json">Especificacion OpenAPI (JSON)</a></li>
  <li><a href="https://normativa.dev">Web del proyecto</a></li>
</ul>
<p>Fuente: <a href="https://www.boe.es/datosabiertos/">API de datos abiertos del BOE</a></p>
</body></html>"""


# ---------------------------------------------------------------------------
# Dominios
# ---------------------------------------------------------------------------

@app.get(
    "/api/dominios",
    summary="Listar dominios tematicos",
    description=(
        "Devuelve todos los dominios juridicos disponibles (fiscal, laboral, mercantil, etc.) "
        "con su descripcion, subtemas y leyes clave pre-mapeadas."
    ),
    tags=["dominios"],
)
async def api_listar_dominios():
    from normativa.tools.domain import listar_dominios
    result = await listar_dominios()
    return _handle_error(result)


# ---------------------------------------------------------------------------
# Busqueda
# ---------------------------------------------------------------------------

@app.get(
    "/api/buscar",
    summary="Buscar por dominio tematico",
    description=(
        "Busca legislacion por dominio juridico. En vez de construir queries complejas, "
        "indica el dominio y normativa selecciona automaticamente los terminos adecuados. "
        "Dominios: laboral, fiscal, mercantil, autonomos, administrativo, penal, civil, "
        "proteccion_datos, digital, vivienda, medioambiental, consumo."
    ),
    tags=["busqueda"],
)
async def api_buscar_por_dominio(
    dominio: str = Query("", description="Clave del dominio (ej: fiscal, laboral)"),
    subtema: str = Query("", description="Subtema dentro del dominio (ej: irpf, despido)"),
    caso: str = Query("", description="Descripcion libre del caso de uso"),
):
    from normativa.tools.search import buscar_por_dominio
    result = await buscar_por_dominio(dominio=dominio, subtema=subtema, caso_uso=caso)
    return _handle_error(result)


@app.get(
    "/api/buscar/texto",
    summary="Busqueda de texto libre en legislacion",
    description=(
        "Busca en toda la legislacion consolidada del BOE por texto libre. "
        "Permite filtrar por rango (Ley, Real Decreto...), departamento, "
        "ambito territorial y rango de fechas."
    ),
    tags=["busqueda"],
)
async def api_buscar_legislacion(
    q: str = Query(..., description="Texto de busqueda (ej: proteccion datos personales)"),
    limit: int = Query(10, ge=1, le=50, description="Maximo de resultados (1-50)"),
    rango: str = Query("", description="Tipo de norma: Ley, Real Decreto, Orden..."),
    departamento: str = Query("", description="Organismo emisor"),
    fecha_desde: str = Query("", description="Fecha inicio YYYYMMDD"),
    fecha_hasta: str = Query("", description="Fecha fin YYYYMMDD"),
    offset: int = Query(0, ge=0, description="Desplazamiento para paginacion"),
):
    from normativa.tools.search import buscar_legislacion
    result = await buscar_legislacion(
        query=q,
        limit=limit,
        rango=rango,
        departamento=departamento,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        offset=offset,
    )
    return _handle_error(result)


# ---------------------------------------------------------------------------
# Metadatos y analisis
# ---------------------------------------------------------------------------

@app.get(
    "/api/norma/{boe_id}/metadatos",
    summary="Metadatos de una disposicion",
    description=(
        "Obtiene metadatos completos de una disposicion del BOE: titulo, rango, "
        "fecha de publicacion, departamento, estado de consolidacion, materias y URL ELI."
    ),
    tags=["normas"],
)
async def api_obtener_metadatos(
    boe_id: str = Path(..., description="Identificador BOE (ej: BOE-A-2006-20764)"),
):
    from normativa.tools.metadata import obtener_metadatos
    result = await obtener_metadatos(boe_id=boe_id)
    return _handle_error(result)


@app.get(
    "/api/norma/{boe_id}/analisis",
    summary="Analisis juridico de una disposicion",
    description=(
        "Obtiene materias, notas y referencias cruzadas de una disposicion: "
        "que normas afecta y por cuales es afectada."
    ),
    tags=["normas"],
)
async def api_obtener_analisis(
    boe_id: str = Path(..., description="Identificador BOE (ej: BOE-A-2006-20764)"),
    incluir_referencias: bool = Query(True, description="Incluir normas que afecta/es afectada"),
    max_referencias: int = Query(20, ge=1, le=100, description="Limite de referencias por tipo"),
):
    from normativa.tools.metadata import obtener_analisis
    result = await obtener_analisis(
        boe_id=boe_id,
        incluir_referencias=incluir_referencias,
        max_referencias=max_referencias,
    )
    return _handle_error(result)


# ---------------------------------------------------------------------------
# Lectura de textos
# ---------------------------------------------------------------------------

@app.get(
    "/api/norma/{boe_id}/indice",
    summary="Indice de una norma consolidada",
    description=(
        "Devuelve la tabla de contenidos (lista de articulos/bloques) de una norma, "
        "con id y titulo de cada bloque. Usa el id para leer articulos individuales."
    ),
    tags=["textos"],
)
async def api_leer_indice(
    boe_id: str = Path(..., description="Identificador BOE (ej: BOE-A-2006-20764)"),
):
    from normativa.tools.text import leer_indice
    result = await leer_indice(boe_id=boe_id)
    return _handle_error(result)


@app.get(
    "/api/norma/{boe_id}/articulo/{bloque}",
    summary="Leer un articulo concreto",
    description=(
        "Lee el texto de UN articulo/bloque de una norma en formato Markdown limpio. "
        "Obtiene el bloque_id del indice (leer_indice)."
    ),
    tags=["textos"],
)
async def api_leer_articulo(
    boe_id: str = Path(..., description="Identificador BOE (ej: BOE-A-2014-12328)"),
    bloque: str = Path(..., description="ID del bloque/articulo (ej: a29)"),
):
    from normativa.tools.text import leer_articulo
    result = await leer_articulo(boe_id=boe_id, bloque_id=bloque)
    return _handle_error(result)


@app.get(
    "/api/norma/{boe_id}/articulos",
    summary="Leer rango de articulos consecutivos",
    description=(
        "Lee un rango consecutivo de articulos de una norma (ej: del a1 al a5). "
        "Limitado a max_bloques para no saturar la respuesta."
    ),
    tags=["textos"],
)
async def api_leer_articulos_rango(
    boe_id: str = Path(..., description="Identificador BOE"),
    desde: str = Query(..., description="ID del primer bloque (ej: a1)"),
    hasta: str = Query(..., description="ID del ultimo bloque (ej: a5)"),
    max_bloques: int = Query(10, ge=1, le=20, description="Maximo bloques a leer (1-20)"),
):
    from normativa.tools.text import leer_articulos_rango
    result = await leer_articulos_rango(
        boe_id=boe_id,
        desde=desde,
        hasta=hasta,
        max_bloques=max_bloques,
    )
    return _handle_error(result)


# ---------------------------------------------------------------------------
# Sumarios diarios
# ---------------------------------------------------------------------------

@app.get(
    "/api/boe/sumario/{fecha}",
    summary="Sumario diario del BOE",
    description=(
        "Consulta las disposiciones publicadas en el BOE en una fecha concreta. "
        "Filtrable por seccion, departamento o dominio tematico. "
        "Formato de fecha: YYYY-MM-DD, DD/MM/YYYY o YYYYMMDD."
    ),
    tags=["sumarios"],
)
async def api_sumario_boe(
    fecha: str = Path(..., description="Fecha del sumario (ej: 2026-04-01)"),
    seccion: str = Query("", description="Seccion del BOE (I, II, III, IV, V)"),
    departamento: str = Query("", description="Departamento emisor"),
    dominio: str = Query("", description="Dominio tematico para filtrar"),
):
    from normativa.tools.summary import sumario_boe
    result = await sumario_boe(
        fecha=fecha,
        seccion=seccion,
        departamento=departamento,
        dominio=dominio,
    )
    return _handle_error(result)


@app.get(
    "/api/borme/sumario/{fecha}",
    summary="Sumario diario del BORME",
    description=(
        "Consulta los actos mercantiles publicados en el BORME "
        "(Boletin Oficial del Registro Mercantil) en una fecha concreta."
    ),
    tags=["sumarios"],
)
async def api_sumario_borme(
    fecha: str = Path(..., description="Fecha del sumario (ej: 2026-04-01)"),
):
    from normativa.tools.summary import sumario_borme
    result = await sumario_borme(fecha=fecha)
    return _handle_error(result)


# ---------------------------------------------------------------------------
# Datos auxiliares
# ---------------------------------------------------------------------------

@app.get(
    "/api/auxiliar/{tipo}",
    summary="Datos auxiliares de referencia del BOE",
    description=(
        "Consulta datos auxiliares: materias (temas juridicos), departamentos "
        "(organismos emisores), rangos (tipos de norma) o ambitos (territoriales)."
    ),
    tags=["auxiliar"],
)
async def api_datos_auxiliares(
    tipo: str = Path(
        ...,
        description="Tipo de dato: materias, departamentos, rangos o ambitos",
    ),
    buscar: str = Query("", description="Texto para filtrar resultados"),
):
    from normativa.tools.auxiliary import datos_auxiliares
    result = await datos_auxiliares(tipo=tipo, buscar=buscar)
    return _handle_error(result)


# ---------------------------------------------------------------------------
# Error handler global
# ---------------------------------------------------------------------------

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "detalle": "Error interno del servidor"},
    )
