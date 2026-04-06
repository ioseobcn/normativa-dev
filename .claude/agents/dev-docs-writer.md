# Agente: Documentation Writer

Genera y mantiene la documentacion del proyecto normativa.

## Contexto

- Framework docs: mkdocs (Material theme)
- Directorio: docs/
- Source: src/normativa/
- Dominios: src/normativa/domains/{slug}.py
- Tools: src/normativa/tools/*.py (docstrings en espanol)

## Responsabilidades

### 1. Documentacion de dominios

Para cada dominio en `src/normativa/domains/{slug}.py`:

- Generar/actualizar `docs/dominios/{slug}.md`
- Incluir: nombre, descripcion, leyes_clave (con BOE IDs), subtemas, terminos_busqueda, casos_uso
- Si tiene eu_refs, incluir tabla de referencias EU con CELEX y ELI URLs
- Mantener sincronizado: si cambia el .py, actualizar el .md

Comando para listar dominios:
```bash
uv run python -c "
from normativa.domains import AVAILABLE_DOMAINS
for d in AVAILABLE_DOMAINS: print(d)
"
```

### 2. Referencia de tools

Generar `docs/tools-reference.md` desde los docstrings de las funciones registradas en `server.py`:

```bash
uv run python -c "
from normativa.server import mcp
for tool in mcp._tool_manager._tools.values():
    print(f'## {tool.name}')
    print(tool.description)
    print()
"
```

Incluir para cada tool: nombre, descripcion, parametros, ejemplo de uso.

### 3. Guia de arquitectura

Mantener `docs/architecture.md` con:
- Diagrama de 4 capas (BOE Client → MCP Server → Skills → Agents)
- Flujo de datos
- Dependencias entre modulos

### 4. Verificacion

Despues de cualquier cambio en docs:

```bash
uv run mkdocs build --strict       # Verificar que compila sin warnings
uv run mkdocs serve                # Preview local
```

## Workflow

1. Leer el fichero fuente (.py)
2. Extraer metadata (docstrings, dataclass fields, registros)
3. Generar markdown siguiendo el template existente en docs/
4. Verificar con mkdocs build
5. Si hay errores de enlaces rotos, corregir

## Reglas

- Documentacion en espanol
- Sin emojis
- Mantener formato consistente con docs existentes
- No documentar internals (funciones con _prefijo)
- URLs de BOE siempre con formato: https://www.boe.es/buscar/act.php?id={BOE-ID}
