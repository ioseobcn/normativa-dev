"""CLI para normativa — acceso rapido a legislacion espanola desde terminal."""

from __future__ import annotations

import asyncio
import json
import sys
from typing import Any

import click


def _run(coro: Any) -> Any:
    """Ejecuta una coroutine en el event loop."""
    return asyncio.run(coro)


def _print_json(data: dict) -> None:
    """Imprime resultado como JSON indentado."""
    click.echo(json.dumps(data, ensure_ascii=False, indent=2))


def _print_tabla(items: list[dict], campos: list[str] | None = None) -> None:
    """Imprime una tabla simple de resultados."""
    if not items:
        click.echo("Sin resultados.")
        return

    if campos is None:
        campos = list(items[0].keys())

    for i, item in enumerate(items, 1):
        click.echo(f"\n--- {i} ---")
        for campo in campos:
            valor = item.get(campo, "")
            if valor:
                click.echo(f"  {campo}: {valor}")


@click.group()
@click.version_option(package_name="normativa")
def main() -> None:
    """normativa: legislacion espanola consolidada con dominios tematicos."""


@main.command()
@click.argument("texto")
@click.option("--dominio", "-d", default="", help="Filtrar por dominio tematico")
@click.option("--limit", "-n", default=10, help="Maximo resultados")
@click.option("--rango", default="", help="Tipo de norma (Ley, Real Decreto...)")
@click.option("--json", "as_json", is_flag=True, help="Salida JSON")
def buscar(texto: str, dominio: str, limit: int, rango: str, as_json: bool) -> None:
    """Busca legislacion por texto libre."""
    from normativa.tools.search import buscar_legislacion, buscar_por_dominio

    if dominio:
        resultado = _run(buscar_por_dominio(dominio=dominio, caso_uso=texto))
    else:
        resultado = _run(buscar_legislacion(query=texto, limit=limit, rango=rango))

    if as_json:
        _print_json(resultado)
    else:
        if "error" in resultado:
            click.echo(f"Error: {resultado['error']}", err=True)
            sys.exit(1)
        items = resultado.get("resultados", [])
        click.echo(f"Total: {resultado.get('total', len(items))}")
        _print_tabla(items, ["boe_id", "titulo", "rango", "fecha", "estado"])


@main.command()
@click.argument("nombre", default="")
@click.option("--subtema", "-s", default="", help="Mostrar subtemas de un dominio")
def dominio(nombre: str, subtema: str) -> None:
    """Lista dominios tematicos o busca por dominio."""
    from normativa.tools.domain import listar_dominios
    from normativa.tools.search import buscar_por_dominio

    if nombre:
        resultado = _run(buscar_por_dominio(dominio=nombre, subtema=subtema))
        if "error" in resultado:
            click.echo(f"Error: {resultado['error']}", err=True)
            if "dominios_disponibles" in resultado:
                click.echo(f"Disponibles: {', '.join(resultado['dominios_disponibles'])}")
            sys.exit(1)
        click.echo(f"Dominio: {resultado.get('nombre_dominio', nombre)}")
        click.echo(f"Query: {resultado.get('query_generada', '')}")
        items = resultado.get("resultados", [])
        _print_tabla(items, ["boe_id", "titulo", "rango", "fecha"])
    else:
        resultado = _run(listar_dominios())
        for dom in resultado.get("dominios", []):
            click.echo(f"\n  {dom['clave']:20s} {dom['nombre']}")
            click.echo(f"  {'':20s} {dom['descripcion']}")
            if dom.get("subtemas"):
                click.echo(f"  {'':20s} Subtemas: {', '.join(dom['subtemas'])}")


@main.command()
@click.argument("boe_id")
@click.argument("bloque_id")
@click.option("--json", "as_json", is_flag=True, help="Salida JSON")
def articulo(boe_id: str, bloque_id: str, as_json: bool) -> None:
    """Lee un articulo concreto de una norma."""
    from normativa.tools.text import leer_articulo

    resultado = _run(leer_articulo(boe_id=boe_id, bloque_id=bloque_id))

    if as_json:
        _print_json(resultado)
    else:
        if "error" in resultado:
            click.echo(f"Error: {resultado['error']}", err=True)
            sys.exit(1)
        click.echo(f"# {resultado.get('titulo', bloque_id)}\n")
        click.echo(resultado.get("texto", ""))


@main.command()
@click.argument("boe_id")
@click.option("--json", "as_json", is_flag=True, help="Salida JSON")
def indice(boe_id: str, as_json: bool) -> None:
    """Muestra el indice de una norma consolidada."""
    from normativa.tools.text import leer_indice

    resultado = _run(leer_indice(boe_id=boe_id))

    if as_json:
        _print_json(resultado)
    else:
        if "error" in resultado:
            click.echo(f"Error: {resultado['error']}", err=True)
            sys.exit(1)
        click.echo(f"Indice de {boe_id} ({resultado.get('total_bloques', 0)} bloques):\n")
        for item in resultado.get("indice", []):
            click.echo(f"  {item['id']:10s} {item['titulo']}")


@main.command()
@click.argument("fecha", default="")
@click.option("--dominio", "-d", default="", help="Filtrar por dominio tematico")
@click.option("--seccion", "-s", default="", help="Filtrar por seccion BOE")
@click.option("--json", "as_json", is_flag=True, help="Salida JSON")
def sumario(fecha: str, dominio: str, seccion: str, as_json: bool) -> None:
    """Muestra el sumario BOE del dia (o fecha indicada)."""
    from normativa.tools.summary import sumario_boe

    resultado = _run(sumario_boe(fecha=fecha, seccion=seccion, dominio=dominio))

    if as_json:
        _print_json(resultado)
    else:
        if "error" in resultado:
            click.echo(f"Error: {resultado['error']}", err=True)
            sys.exit(1)
        click.echo(f"Sumario BOE {resultado.get('fecha', '')} ({resultado.get('total', 0)} entradas):\n")
        _print_tabla(
            resultado.get("entradas", []),
            ["boe_id", "titulo", "seccion", "departamento"],
        )


@main.command()
@click.option(
    "--mode",
    type=click.Choice(["mcp", "http"]),
    default="mcp",
    help="Modo de transporte: mcp (stdio, default) o http (REST API).",
)
@click.option(
    "--port",
    default=8787,
    type=int,
    help="Puerto para el servidor HTTP (default 8787).",
)
@click.option(
    "--host",
    default="0.0.0.0",
    help="Host para el servidor HTTP (default 0.0.0.0).",
)
def serve(mode: str, port: int, host: str) -> None:
    """Inicia el servidor MCP (stdio) o HTTP (REST API)."""
    if mode == "http":
        try:
            import uvicorn
        except ImportError:
            click.echo(
                "Error: uvicorn no instalado. Instala con: pip install 'normativa[http]'",
                err=True,
            )
            sys.exit(1)
        click.echo(f"Iniciando API HTTP en http://{host}:{port}")
        click.echo(f"Documentacion: http://{host}:{port}/docs")
        click.echo(f"OpenAPI spec:  http://{host}:{port}/api/openapi.json")
        uvicorn.run("normativa.api:app", host=host, port=port, log_level="info")
    else:
        from normativa.server import mcp
        mcp.run()


if __name__ == "__main__":
    main()
