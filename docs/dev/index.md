# Vision general del desarrollo

Esta documentacion esta dirigida a desarrolladores que quieren entender, modificar o
contribuir al proyecto **normativa**. Si solo quieres usar la herramienta, consulta
la [guia de inicio rapido](../guide/quickstart.md).

## Arquitectura en 4 capas

```
                         Usuario / LLM
                              |
            +-----------------+-----------------+
            |           Capa 4: Agentes          |
            |  .claude/agents/ (6 legal + 3 dev) |
            |  Pipeline: investigador -> extractor|
            |  -> analista -> redactor            |
            +-----------------+-----------------+
                              |
            +-----------------+-----------------+
            |           Capa 3: Skills           |
            |  .claude/skills/ (8 dominios +     |
            |  2 dev + 1 API ref)                |
            |  Lazy-loaded por analista-dominio   |
            +-----------------+-----------------+
                              |
            +-----------------+-----------------+
            |     Capa 2: MCP Server + CLI       |
            |  server.py (11 tools FastMCP)       |
            |  cli.py (Click commands)            |
            |  tools/*.py (implementacion)        |
            |  cache.py (SQLite TTL)              |
            |  xml_parser.py (XML -> Markdown)    |
            +-----------------+-----------------+
                              |
            +-----------------+-----------------+
            |     Capa 1: BOE API Client         |
            |  boe_client.py (httpx async)        |
            |  Retry + rate limit 2 req/s         |
            |  Base: boe.es/datosabiertos/api     |
            +-----------------+-----------------+
                              |
                      API del BOE (REST)
```

## Mapa de ficheros

| Fichero | Responsabilidad |
|---------|----------------|
| `src/normativa/boe_client.py` | HTTP async client para la API del BOE. Retry con backoff, rate limiting, gestion de JSON y XML. |
| `src/normativa/xml_parser.py` | Convierte bloques XML del BOE a Markdown limpio. Mapea clases CSS a formatos de texto. |
| `src/normativa/cache.py` | Cache SQLite con TTL por tabla. Patron `get_or_fetch` que cachea automaticamente. |
| `src/normativa/registry.py` | Carga dominios tematicos por nombre. Busqueda multi-dominio por scoring de palabras clave. |
| `src/normativa/server.py` | Registra las 11 tools en FastMCP. Punto de entrada del servidor MCP. |
| `src/normativa/cli.py` | CLI basado en Click: `buscar`, `dominio`, `articulo`, `indice`, `sumario`, `serve`. |
| `src/normativa/domains/_base.py` | Dataclasses: `DomainConfig`, `LeyRef`, `Subtema`, `EURef`. |
| `src/normativa/domains/__init__.py` | Registro `AVAILABLE_DOMAINS` (con DomainConfig) y `DOMINIOS` (diccionarios simples). |
| `src/normativa/domains/{slug}.py` | Definicion de cada dominio tematico con leyes, articulos, subtemas y EU refs. |
| `src/normativa/tools/_shared.py` | Singletons lazy para `BOEClient` y `Cache`, compartidos entre todas las tools. |
| `src/normativa/tools/search.py` | `buscar_legislacion` y `buscar_por_dominio` (el diferenciador clave del proyecto). |
| `src/normativa/tools/text.py` | `leer_indice`, `leer_articulo`, `leer_articulos_rango` -- las tools mas criticas. |
| `src/normativa/tools/metadata.py` | `obtener_metadatos` y `obtener_analisis` (vigencia, referencias cruzadas). |
| `src/normativa/tools/summary.py` | `sumario_boe` y `sumario_borme` (publicaciones diarias). |
| `src/normativa/tools/domain.py` | `listar_dominios` (listado con enriquecimiento desde DomainConfig). |
| `src/normativa/tools/auxiliary.py` | `datos_auxiliares` (tablas de referencia del BOE). |
| `tests/conftest.py` | Fixtures compartidas: XML samples reales, JSON mocks, mock del BOEClient. |

## Decisiones de diseno clave

### Por que dominios tematicos

La API del BOE no tiene filtrado por materia en el listing de legislacion, y su
busqueda por texto libre devuelve 500 para muchas consultas. Los dominios resuelven
esto: cada dominio mapea leyes concretas con sus BOE IDs verificados, articulos
clave, terminos de busqueda y materias. Cuando el LLM pregunta por "IVA servicios
digitales", normativa sabe exactamente que ley abrir y que articulos leer.

### Por que cache SQLite con TTL

Las leyes consolidadas cambian poco (se actualizan cuando hay reforma), pero los
sumarios diarios son efimeros. El cache con TTL diferenciado por tabla permite que
los metadatos se refresquen semanalmente (168h), los bloques de texto cada 3 dias
(72h), y los sumarios nunca expiren (son inmutables por fecha).

### Por que XML a Markdown y no HTML

Los LLMs procesan Markdown mucho mejor que HTML. El BOE solo devuelve texto como XML,
asi que el parser convierte las clases CSS (`articulo`, `parrafo`, `parrafo_2`,
`parrafo_3`) a encabezados y niveles de indentacion en Markdown. Esto mantiene el
contexto del LLM limpio y compacto.

### Por que tools como funciones y no clases

FastMCP registra funciones directamente. Las tools son funciones async que reciben
parametros tipados y devuelven `dict[str, Any]`. Los errores se devuelven como
`{"error": "...", "tool": "nombre"}` en lugar de lanzar excepciones, porque el
protocolo MCP no maneja excepciones Python.

### Por que dos sistemas de dominios (DOMINIOS + DomainConfig)

`DOMINIOS` es el diccionario simple original con keywords y subtemas como strings.
`DomainConfig` (via `AVAILABLE_DOMAINS`) es el sistema enriquecido con BOE IDs reales,
articulos clave verificados, y EU refs. Los 7 dominios enriquecidos coexisten con
los 14 dominios simples. Los 7 adicionales se migraran a DomainConfig en futuras
versiones.

## Flujo de datos

```
1. Query del usuario: "Que IVA aplica a servicios digitales?"
                |
2. buscar_por_dominio(dominio="fiscal", subtema="iva")
                |
3. registry.search_domains("IVA servicios digitales")
   -> Identifica dominio "fiscal", subtema "iva"
   -> Extrae leyes_clave del DomainConfig
   -> Construye query con keywords del dominio
                |
4. BOEClient.legislacion_lista(query=..., limit=15)
   -> GET /legislacion-consolidada?query=...&limit=15
   -> Retry si 5xx, backoff exponencial
   -> Rate limit: max 2 req/s
                |
   [Si la API falla: fallback a leyes del registro local]
                |
5. Cache.get_or_fetch("indices", boe_id, fetch_fn)
   -> Si cached y no expirado: devuelve directo
   -> Si miss: llama a fetch_fn, almacena en SQLite
                |
6. xml_parser.parse_bloque(xml_text)
   -> <p class="articulo"> -> "## Titulo"
   -> <p class="parrafo">  -> texto plano
   -> <p class="parrafo_2"> -> "  texto indentado"
                |
7. Respuesta: dict con boe_id, titulo, texto Markdown, version
```

## Paginas de esta seccion

- [Arquitectura](architecture.md) -- documentacion profunda de cada componente
- [API del BOE (internals)](boe-api-internals.md) -- lo que descubrimos sobre la API
- [Crear dominios](domain-authoring.md) -- guia paso a paso para nuevos dominios
- [Testing](testing.md) -- como escribir y ejecutar tests
- [Agentes y skills](agents-and-skills.md) -- sistema de agentes y skills para Claude
- [Integracion EU](eu-integration.md) -- estado de la integracion con legislacion europea
