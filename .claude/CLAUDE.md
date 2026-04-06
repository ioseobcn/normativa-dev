# normativa — Legislacion espanola tematica

MCP Server + CLI + Agent Team para legislacion espanola consolidada via API del BOE.
Web: normativa.dev | PyPI: normativa | Licencia: MIT

## Arquitectura (4 capas)

Capa 1: BOE API Client (src/normativa/boe_client.py)
  - httpx async, retry, rate limit 2 req/s
  - Base: https://www.boe.es/datosabiertos/api
  - Endpoints: /legislacion-consolidada, /boe/sumario/{fecha}, /datos-auxiliares/{tipo}

Capa 2: MCP Server (src/normativa/server.py + tools/)
  - 11 tools FastMCP (buscar_por_dominio es el diferencial)
  - Cache SQLite en ~/.cache/normativa/cache.db
  - XML parser para bloques de texto → markdown

Capa 3: Skills (.claude/skills/)
  - 8 packs de conocimiento de dominio (lazy-loaded)
  - Solo el analista-dominio los carga

Capa 4: Agent Team (.claude/agents/)
  - 6 agentes en pipeline: investigador → extractor → analista → redactor
  - Comunicacion via handoff/ (referencias, no texto completo)

## Ficheros clave

| Fichero | Responsabilidad |
|---------|----------------|
| src/normativa/boe_client.py | HTTP async client para API BOE |
| src/normativa/xml_parser.py | XML bloque → markdown limpio |
| src/normativa/cache.py | Cache SQLite con TTL |
| src/normativa/registry.py | Cargador de dominios tematicos |
| src/normativa/server.py | FastMCP server (11 tools) |
| src/normativa/cli.py | CLI click |
| src/normativa/domains/_base.py | Dataclasses: DomainConfig, LeyRef, Subtema, EURef |
| src/normativa/domains/{nombre}.py | Definicion de cada dominio (leyes, articulos, materias) |
| src/normativa/tools/*.py | Implementacion de cada tool MCP |

## API del BOE — Referencia rapida

Endpoints verificados:
- GET /legislacion-consolidada?limit=N&offset=N&from=YYYYMMDD&to=YYYYMMDD
- GET /legislacion-consolidada/id/{BOE-ID}/metadatos (JSON)
- GET /legislacion-consolidada/id/{BOE-ID}/analisis (JSON)
- GET /legislacion-consolidada/id/{BOE-ID}/texto/indice (JSON)
- GET /legislacion-consolidada/id/{BOE-ID}/texto/bloque/{bloque_id} (XML ONLY)
- GET /boe/sumario/{YYYYMMDD} (JSON)
- GET /datos-auxiliares/materias|departamentos|rangos|ambitos (JSON)

Limitaciones:
- El param `query` en /legislacion-consolidada devuelve 500 para muchas consultas
- Materias NO son filtrables en listing (solo en /analisis por documento)
- Texto SOLO en XML — los endpoints /texto/ solo aceptan application/xml
- IDs de bloque varian: a1, a10, tpreliminar, dfquinta, dtercera

## Dominios tematicos

7 dominios con 17 leyes mapeadas y 226+ articulos clave:
fiscal, laboral, mercantil, autonomos, proteccion_datos, digital, vivienda

Para anadir un nuevo dominio: crear src/normativa/domains/{slug}.py siguiendo el patron de fiscal.py + anadir slug a domains/__init__.py AVAILABLE_DOMAINS + crear skill en .claude/skills/dominio-{slug}.md

## Reglas de desarrollo

- Python 3.11+ / uv como package manager
- Tests: uv run pytest
- Nunca cargar leyes completas en contexto (leer_indice → leer_articulo)
- Max 10 bloques por extraccion
- Docstrings de tools en espanol (son la descripcion que ven los LLMs)
- Imports: from normativa.boe_client import BOEClient
- Los tools son funciones async, no metodos de clase
- Errores: devolver dict con "error", nunca raise al MCP

## Comandos utiles

```bash
uv sync                           # Instalar dependencias
uv run pytest                     # Tests
uv run python -m normativa        # Iniciar MCP server
uv run normativa buscar "irpf"    # CLI
uv run python -c "
from normativa.registry import list_domains
for d in list_domains(): print(d['slug'], d['nombre'])
"
```

## Equipo de agentes

### Para uso legal (consultas de legislacion)
- investigador-legal → extractor-articulos → analista-dominio → redactor-informes
- verificador-cumplimiento (compliance checks)
- monitor-cambios (novedades BOE)

### Para desarrollo
- dev-contributor: contribuir al proyecto (anadir dominios, mejorar tools, corregir bugs)
- dev-domain-builder: construir nuevos dominios tematicos completos
- dev-tester: ejecutar y crear tests

## Pipeline estandar (consultas legales)

```
Fase 1 (paralelo): investigador-legal + monitor-cambios
Fase 2:            extractor-articulos
Fase 3 (paralelo): analista-dominio + verificador-cumplimiento
Fase 4:            redactor-informes
```

## Directorio handoff/

Los agentes se comunican via archivos en `handoff/`:
- `investigacion-{slug}.md` — resultado del investigador
- `extracto-{slug}.md` — texto de articulos extraidos
- `analisis-{slug}.md` — interpretacion del analista
- `cumplimiento-{slug}.md` — checklist de cumplimiento
- `cambios-{dominio}-{fecha}.md` — cambios legislativos detectados
- `informe-{slug}.md` — informe final

## Disclaimer estandar

> Este documento tiene caracter meramente informativo y no constituye asesoramiento juridico profesional. Las conclusiones se basan en la legislacion vigente a fecha de consulta y pueden verse afectadas por cambios normativos, jurisprudencia o interpretaciones administrativas posteriores. Consulte con un profesional cualificado antes de tomar decisiones basadas en este analisis.

## Contribuir al proyecto

### Anadir un nuevo dominio

1. Crear `src/normativa/domains/{slug}.py` siguiendo el patron de `fiscal.py`
2. Definir `DOMAIN = DomainConfig(...)` con leyes_clave, subtemas, terminos_busqueda, casos_uso
3. Anadir el slug a `AVAILABLE_DOMAINS` en `src/normativa/domains/__init__.py`
4. Crear skill `.claude/skills/dominio-{slug}.md`
5. Anadir tests en `tests/test_registry.py` (verificar carga, busqueda)
6. Verificar: `uv run python -c "from normativa.registry import load_domain; print(load_domain('{slug}'))"`

### Anadir una nueva tool MCP

1. Crear funcion async en `src/normativa/tools/{modulo}.py`
2. La funcion debe devolver `dict[str, Any]` — errores como `{"error": "...", "tool": "nombre"}`
3. Registrar en `src/normativa/server.py` con `mcp.tool()(funcion)`
4. Docstring en espanol (es la descripcion visible para LLMs)
5. Anadir tests en `tests/test_tools/test_{modulo}.py`

### Anadir tests

- Tests en `tests/` con pytest + pytest-asyncio
- Fixtures en `tests/conftest.py` (XML samples, JSON mocks, mock clients)
- Mock HTTP con `pytest-httpx` — nunca llamadas reales a la API en tests
- Patron: funcion async → `await funcion(...)` → assert sobre el dict resultado

## Testing

```bash
uv run pytest                     # Todos los tests
uv run pytest -v                  # Verbose
uv run pytest tests/test_xml_parser.py  # Un fichero
uv run pytest -k "test_fiscal"    # Por nombre
```

### Patrones de fixtures

- `sample_bloque_xml`: XML real de un bloque BOE (Art. 29 LIS)
- `sample_metadatos_json`: JSON de respuesta /metadatos
- `sample_indice_json`: JSON de respuesta /indice
- `mock_boe_client`: async mock que devuelve fixtures sin HTTP

### Convenios

- `asyncio_mode = "auto"` en pyproject.toml — no hace falta `@pytest.mark.asyncio`
- Fixtures async usan `@pytest.fixture`
- Tests que necesitan cache usan `tmp_path` para DB temporal

## Release process

1. Bump version en `src/normativa/__init__.py` y `pyproject.toml`
2. Actualizar CHANGELOG.md (formato Keep a Changelog)
3. Commit: `git commit -m "release: vX.Y.Z"`
4. Tag: `git tag vX.Y.Z`
5. Build: `uv build`
6. Publish: `uv publish`
7. Push: `git push && git push --tags`
8. GitHub release: `gh release create vX.Y.Z --generate-notes`

## Documentacion

```bash
uv run mkdocs serve               # Preview local en http://localhost:8000
uv run mkdocs build                # Build estatico en site/
```

- Docs en `docs/` (Markdown)
- Documentacion de dominios: un .md por dominio, sincronizado con el .py
- Referencia de tools: generada desde docstrings de server.py
- Editar `mkdocs.yml` para estructura de navegacion
