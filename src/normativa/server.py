"""FastMCP server para normativa — legislacion espanola consolidada."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from normativa.tools.search import buscar_legislacion, buscar_por_dominio
from normativa.tools.metadata import obtener_metadatos, obtener_analisis
from normativa.tools.text import leer_indice, leer_articulo, leer_articulos_rango
from normativa.tools.summary import sumario_boe, sumario_borme
from normativa.tools.domain import listar_dominios
from normativa.tools.auxiliary import datos_auxiliares

mcp = FastMCP("normativa")

# ---------------------------------------------------------------------------
# Registro de herramientas
#
# Cada tool es una funcion async que devuelve dict. FastMCP se encarga
# de serializar a JSON y exponer via MCP.
# ---------------------------------------------------------------------------

# -- Busqueda ---------------------------------------------------------------

mcp.tool()(buscar_legislacion)
mcp.tool()(buscar_por_dominio)

# -- Metadatos y analisis ---------------------------------------------------

mcp.tool()(obtener_metadatos)
mcp.tool()(obtener_analisis)

# -- Lectura de textos (las mas criticas) -----------------------------------

mcp.tool()(leer_indice)
mcp.tool()(leer_articulo)
mcp.tool()(leer_articulos_rango)

# -- Sumarios diarios -------------------------------------------------------

mcp.tool()(sumario_boe)
mcp.tool()(sumario_borme)

# -- Dominios y auxiliares --------------------------------------------------

mcp.tool()(listar_dominios)
mcp.tool()(datos_auxiliares)
