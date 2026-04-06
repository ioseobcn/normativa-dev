# Arquitectura

Documentacion profunda de cada componente del sistema normativa.

## BOE API Client (`boe_client.py`)

### Responsabilidad

Unico punto de acceso HTTP a la API de datos abiertos del BOE
(`https://www.boe.es/datosabiertos/api`). Todo el trafico HTTP del proyecto
pasa por esta clase.

### Patron: async context manager

```python
async with BOEClient() as boe:
    meta = await boe.legislacion_metadatos("BOE-A-2006-20764")
```

El client se crea como context manager que inicializa un `httpx.AsyncClient`
en `__aenter__` y lo cierra en `__aexit__`. Esto garantiza que las conexiones
se cierran correctamente aunque haya excepciones.

### Retry con backoff exponencial

Cada peticion pasa por `_request()`, que implementa retry para errores de
servidor (5xx) y errores de transporte (timeouts, conexion):

```python
_MAX_RETRIES = 3
_BACKOFF_BASE = 1.0

for attempt in range(1, _MAX_RETRIES + 1):
    async with self._semaphore:
        try:
            response = await self._client.send(resp)
            response.raise_for_status()
            await asyncio.sleep(1.0 / _MAX_RPS)
            return response
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code < 500:
                raise  # 4xx no se reintenta
            delay = _BACKOFF_BASE * (2 ** (attempt - 1))
            await asyncio.sleep(delay)
```

Los errores 4xx se propagan inmediatamente (son problemas del cliente, no del
servidor). Los delays son: 1s, 2s, 4s.

### Rate limiting

El client usa un `asyncio.Semaphore(_MAX_RPS)` combinado con un sleep tras
cada peticion para espaciar las llamadas:

```python
_MAX_RPS = 2  # max requests per second

self._semaphore = asyncio.Semaphore(_MAX_RPS)

async with self._semaphore:
    # ... hacer peticion ...
    await asyncio.sleep(1.0 / _MAX_RPS)
```

Esto permite maximo 2 peticiones concurrentes, con al menos 0.5s entre cada una.
En la practica, el throughput efectivo es de ~2 req/s.

### Endpoints

| Metodo | Path | Accept | Devuelve |
|--------|------|--------|----------|
| `legislacion_lista()` | `/legislacion-consolidada` | JSON | Lista paginada de normas |
| `legislacion_metadatos()` | `/legislacion-consolidada/id/{id}/metadatos` | JSON | Metadatos de una norma |
| `legislacion_analisis()` | `/legislacion-consolidada/id/{id}/analisis` | JSON | Referencias cruzadas |
| `legislacion_indice()` | `/legislacion-consolidada/id/{id}/texto/indice` | JSON | Tabla de contenidos |
| `legislacion_bloque()` | `/legislacion-consolidada/id/{id}/texto/bloque/{bid}` | XML | Texto de un articulo |
| `sumario_boe()` | `/boe/sumario/{fecha}` | JSON | Sumario diario BOE |
| `sumario_borme()` | `/borme/sumario/{fecha}` | JSON | Sumario diario BORME |
| `datos_auxiliares()` | `/datos-auxiliares/{tipo}` | JSON | Materias, departamentos, rangos, ambitos |

### Detalle: `_get_json` vs `_get_xml`

El client tiene dos metodos internos porque los endpoints de texto del BOE
solo aceptan `application/xml`:

```python
async def _get_json(self, path: str, **params: Any) -> dict:
    params = {k: v for k, v in params.items() if v is not None}
    resp = await self._request(path, params=params or None)
    return resp.json()

async def _get_xml(self, path: str) -> str:
    resp = await self._request(path, accept="application/xml")
    return resp.text
```

`legislacion_bloque()` usa `_get_xml` y devuelve el string XML crudo.
El resto usa `_get_json`.

---

## XML Parser (`xml_parser.py`)

### Responsabilidad

Convierte los bloques XML que devuelve el endpoint `/texto/bloque/` en
diccionarios con el texto en Markdown limpio.

### Estructura XML de un bloque BOE

```xml
<response status="OK">
  <data>
    <bloque id="a29" tipo="precepto" titulo="Articulo 29. Tipo de gravamen.">
      <version id_norma="BOE-A-2014-12328"
               fecha_publicacion="20141128"
               fecha_vigencia="20150101">
        <p class="articulo">Articulo 29. Tipo de gravamen.</p>
        <p class="parrafo">1. El tipo general sera del 25 por ciento.</p>
        <p class="parrafo_2">No obstante, las entidades de nueva creacion...</p>
        <p class="parrafo_3">Se incluyen multas y sanciones.</p>
      </version>
    </bloque>
  </data>
</response>
```

### Mapeo de clases CSS a Markdown

```python
_CLASS_MAP: dict[str, str] = {
    "articulo": "heading",      # -> "## texto"
    "parrafo": "paragraph",     # -> "texto"
    "parrafo_2": "indent_1",    # -> "  texto"  (2 espacios)
    "parrafo_3": "indent_2",    # -> "    texto" (4 espacios)
}
```

Las clases no mapeadas se tratan como `"paragraph"` (texto plano).

### `parse_bloque()` -- funcion principal

Devuelve un diccionario con la estructura del bloque:

```python
{
    "id": "a29",
    "tipo": "precepto",
    "titulo": "Articulo 29. Tipo de gravamen.",
    "version": {
        "id_norma": "BOE-A-2014-12328",
        "fecha_publicacion": "20141128",
        "fecha_vigencia": "20150101",
    },
    "texto_markdown": "## Articulo 29. Tipo de gravamen.\n\n1. El tipo general...",
}
```

La funcion maneja tres variantes de XML:

1. **Con envelope**: `<response><data><bloque>` -- caso normal de la API
2. **Sin envelope**: `<bloque>` como raiz -- XML directo
3. **Sin version**: `<bloque>` con `<p>` directamente dentro (edge case)

### `parse_indice()` -- parseo del indice

El indice viene como JSON pero con estructura variable. `parse_indice()`
normaliza envolviendo el dato que reciba:

```python
# Acepta:
# - dict con {"data": {"items": [...]}}
# - dict con {"items": [...]}
# - lista directa [...]
# Devuelve siempre: list[{"id": "a1", "titulo": "...", "fecha_actualizacion": "..."}]
```

---

## Cache (`cache.py`)

### Responsabilidad

Cache SQLite asincrono con TTL diferenciado por tipo de dato. Usa el patron
`get_or_fetch` para cachear transparentemente las llamadas al BOE.

### Schema SQLite

Cada tabla tiene la misma estructura base:

```sql
CREATE TABLE {tabla} (
    {key_columns} TEXT NOT NULL,
    data TEXT NOT NULL,         -- JSON serializado
    fetched_at TEXT NOT NULL,   -- ISO timestamp UTC
    expires_at TEXT,            -- ISO timestamp UTC o NULL (nunca expira)
    PRIMARY KEY ({key_columns})
)
```

### Tablas y TTL

| Tabla | Claves | TTL (horas) | Notas |
|-------|--------|-------------|-------|
| `metadatos` | `key` (BOE ID) | 168 (7 dias) | Cambian poco pero pueden actualizarse |
| `analisis` | `key` (BOE ID) | 168 (7 dias) | Referencias cruzadas estables |
| `indices` | `key` (BOE ID) | 72 (3 dias) | Pueden anadir articulos nuevos tras reforma |
| `bloques` | `boe_id`, `bloque_id` | 72 (3 dias) | Texto consolidado, cambia con reformas |
| `sumarios` | `tipo`, `fecha` | 0 (nunca) | Inmutables (una fecha = un sumario) |
| `auxiliares` | `key` (tipo) | 720 (30 dias) | Materias y departamentos, muy estables |

### Patron `get_or_fetch`

Es el nucleo del cache. Automatiza el ciclo check-fetch-store:

```python
async def get_or_fetch(
    self,
    table: str,
    key: Any,
    fetch_fn: Callable[[], Awaitable[Any]],
    ttl_hours: int | None = None,
) -> Any:
```

1. Busca en la tabla por la clave
2. Si existe y no ha expirado: devuelve el dato deserializado
3. Si no existe o ha expirado: llama a `fetch_fn()`, serializa a JSON,
   almacena con timestamp, y devuelve

Ejemplo de uso en las tools:

```python
data = await cache.get_or_fetch(
    "bloques", (boe_id, bloque_id),
    lambda: client.legislacion_bloque(boe_id, bloque_id),
)
```

### Claves compuestas

La tabla `bloques` usa clave compuesta `(boe_id, bloque_id)`. La tabla
`sumarios` usa `(tipo, fecha)`. El cache gestiona esto internamente:

```python
_SCHEMAS: dict[str, tuple[list[str], bool]] = {
    "metadatos": (["key"], False),
    "bloques": (["boe_id", "bloque_id"], True),
    "sumarios": (["tipo", "fecha"], True),
}
```

### Invalidacion

```python
# Invalidar una entrada concreta
await cache.invalidate("metadatos", "BOE-A-2006-20764")

# Invalidar toda una tabla
await cache.invalidate("metadatos")
```

### Ruta del fichero

Por defecto: `~/.cache/normativa/cache.db`. Configurable en el constructor:

```python
cache = Cache(path="/ruta/personalizada/cache.db")
```

### WAL mode

El cache activa `PRAGMA journal_mode=WAL` al abrir la conexion, lo que permite
lecturas concurrentes con escrituras sin bloqueos.

---

## Domain Registry (`registry.py`)

### Responsabilidad

Carga dinamicamente los modulos de dominio y proporciona busqueda multi-dominio
con scoring por relevancia.

### Carga lazy de dominios

```python
def load_domain(name: str) -> DomainConfig:
    if name in _cache:
        return _cache[name]
    module = importlib.import_module(f"normativa.domains.{name}")
    config: DomainConfig = getattr(module, "DOMAIN", None)
    _cache[name] = config
    return config
```

Los modulos se cargan una sola vez y se cachean en `_cache` (dict global).
Cada modulo de dominio debe exponer una variable `DOMAIN` de tipo `DomainConfig`.

### Busqueda multi-dominio

`search_domains()` implementa busqueda por scoring de palabras clave. Cada
palabra del query se busca en:

| Campo | Score |
|-------|-------|
| `nombre` / `descripcion` del dominio | +10 |
| `nombre_corto` / `titulo_oficial` de leyes | +9 |
| `slug` / `descripcion` de casos de uso | +8 |
| `nombre` / `descripcion` de subtemas | +7 |
| `slug` / texto de `casos_uso` de subtemas | +6 |
| `terminos_busqueda` del dominio | +5 |
| `terminos_busqueda` de subtemas | +4 |

Los resultados se devuelven ordenados por score descendente. Esto permite que
una query como "RGPD cookies" matchee tanto `proteccion_datos` (por RGPD)
como `digital` (por cookies).

### Dataclasses (`domains/_base.py`)

```python
@dataclass
class EURef:
    celex: str         # "32016R0679" (RGPD)
    titulo: str        # "Reglamento General de Proteccion de Datos"
    tipo: str          # "reglamento", "directiva", "decision"
    eli_url: str = ""  # "http://data.europa.eu/eli/reg/2016/679/oj"
    relacion: str = "transpone"  # "transpone", "implementa", "complementa", "deroga"

@dataclass
class LeyRef:
    boe_id: str              # "BOE-A-2006-20764"
    nombre_corto: str        # "Ley IRPF"
    titulo_oficial: str      # Titulo completo
    rango: str               # "Ley", "Real Decreto", etc.
    articulos_clave: dict[str, str] = field(default_factory=dict)
    eu_refs: list[EURef] = field(default_factory=list)

@dataclass
class Subtema:
    slug: str
    nombre: str
    descripcion: str
    leyes: list[str] = field(default_factory=list)         # BOE IDs
    materias_boe: list[int] = field(default_factory=list)  # Codigos materia
    terminos_busqueda: list[str] = field(default_factory=list)
    casos_uso: list[str] = field(default_factory=list)

@dataclass
class DomainConfig:
    slug: str
    nombre: str
    descripcion: str
    leyes_clave: dict[str, LeyRef] = field(default_factory=dict)
    subtemas: list[Subtema] = field(default_factory=list)
    materias_boe: list[int] = field(default_factory=list)
    departamentos_boe: list[str] = field(default_factory=list)
    terminos_busqueda: list[str] = field(default_factory=list)
    dominios_relacionados: list[str] = field(default_factory=list)
    casos_uso: dict[str, str] = field(default_factory=dict)
```

### Dos sistemas de dominios

El fichero `domains/__init__.py` contiene:

1. **`AVAILABLE_DOMAINS`**: lista de 7 slugs con `DomainConfig` completo (fiscal,
   laboral, mercantil, autonomos, proteccion_datos, digital, vivienda)

2. **`DOMINIOS`**: diccionario con 14 dominios como dicts simples (incluye los 7
   anteriores mas administrativo, penal, civil, medioambiental, tecnologia,
   inmobiliario, consumo)

Las tools buscan primero en `AVAILABLE_DOMAINS` para extraer leyes clave, y
usan `DOMINIOS` como fallback para keywords y subtemas basicos.

---

## MCP Server (`server.py`)

### Responsabilidad

Registra las 11 tools en FastMCP y expone el servidor MCP via stdio.

### Registro de tools

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("normativa")

mcp.tool()(buscar_legislacion)
mcp.tool()(buscar_por_dominio)
mcp.tool()(obtener_metadatos)
mcp.tool()(obtener_analisis)
mcp.tool()(leer_indice)
mcp.tool()(leer_articulo)
mcp.tool()(leer_articulos_rango)
mcp.tool()(sumario_boe)
mcp.tool()(sumario_borme)
mcp.tool()(listar_dominios)
mcp.tool()(datos_auxiliares)
```

FastMCP usa los docstrings de cada funcion como descripcion de la tool.
Los nombres de parametros y sus type hints se convierten automaticamente
en el schema JSON de la tool.

### Flujo de ejecucion de una tool

```
1. Claude envia tool_call con nombre y parametros
2. FastMCP despacha a la funcion async correspondiente
3. La funcion llama a get_client() y get_cache() (singletons)
4. Cache.get_or_fetch() decide si pedir al BOE o usar cache
5. Si hace falta HTTP: BOEClient._request() con retry + rate limit
6. El resultado (dict) se serializa a JSON y se devuelve por MCP
```

### Singletons compartidos (`tools/_shared.py`)

```python
_client: BOEClient | None = None
_cache: Cache | None = None

async def get_client() -> BOEClient:
    global _client
    if _client is None:
        _client = BOEClient()
        await _client.__aenter__()
    return _client

async def get_cache() -> Cache:
    global _cache
    if _cache is None:
        _cache = Cache()
        await _cache.__aenter__()
    return _cache
```

Se crean una sola vez y se reutilizan en todas las llamadas. Esto evita abrir
y cerrar conexiones HTTP y SQLite en cada tool call.

---

## CLI (`cli.py`)

### Responsabilidad

Interfaz de linea de comandos basada en Click. Proporciona acceso rapido sin
necesidad de un LLM.

### Estructura de comandos

```
normativa
  buscar <texto> [-d dominio] [-n limit] [--rango] [--json]
  dominio [nombre] [-s subtema]
  articulo <boe_id> <bloque_id> [--json]
  indice <boe_id> [--json]
  sumario [fecha] [-d dominio] [-s seccion] [--json]
  serve
```

### Patron de ejecucion

Las funciones de las tools son async, pero Click es sincrono. El CLI las
ejecuta con un helper:

```python
def _run(coro: Any) -> Any:
    return asyncio.run(coro)

# Uso:
resultado = _run(buscar_legislacion(query=texto, limit=limit))
```

### Comando `serve`

Inicia el servidor MCP en modo stdio:

```python
@main.command()
def serve() -> None:
    from normativa.server import mcp
    mcp.run()
```
