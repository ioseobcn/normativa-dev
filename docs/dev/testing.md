# Testing

Guia para escribir y ejecutar tests en normativa.

## Ejecutar tests

```bash
# Todos los tests
uv run pytest -v

# Un fichero concreto
uv run pytest tests/test_xml_parser.py

# Filtrar por nombre
uv run pytest -k "test_fiscal"

# Traceback corto
uv run pytest --tb=short

# Solo tests que fallaron la ultima vez
uv run pytest --lf
```

## Configuracion

En `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"

[dependency-groups]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.23",
    "pytest-httpx>=0.30",
    "mkdocs-material>=9.0",
]
```

Con `asyncio_mode = "auto"`, las funciones `async def test_*` se detectan y
ejecutan automaticamente sin necesidad del decorador `@pytest.mark.asyncio`.

## Estructura de tests

```
tests/
  __init__.py
  conftest.py              # Fixtures compartidas
  test_xml_parser.py       # Tests del parser XML/Markdown
  test_registry.py         # Tests del registry de dominios
  test_cache.py            # Tests del cache SQLite
  test_tools/
    __init__.py
    test_search.py         # Tests de buscar_legislacion, buscar_por_dominio
    test_metadata.py       # Tests de obtener_metadatos, obtener_analisis
```

### Convencion de nombres

- Ficheros: `test_{modulo}.py`
- Clases: `TestNombreComponente` (agrupan tests relacionados)
- Metodos: `test_{que}_{condicion}` o `test_{que}_{condicion}_{esperado}`

Ejemplos:

```python
class TestParseBloqueNormal:
    def test_extracts_bloque_id(self, sample_bloque_xml): ...
    def test_converts_articulo_class_to_heading(self, sample_bloque_xml): ...

class TestParseBloqueEdgeCases:
    def test_no_bloque_raises(self): ...
    def test_invalid_xml_raises(self): ...
```

## Fixtures disponibles (`conftest.py`)

### Fixtures XML

XML real de bloques del BOE, extraido de la Ley del Impuesto sobre Sociedades.

| Fixture | Contenido |
|---------|-----------|
| `sample_bloque_xml` | Art. 29 LIS completo con `<response>` envelope, `<version>`, y parrafos con clases `articulo`, `parrafo`, `parrafo_2` |
| `sample_bloque_xml_empty` | Bloque sin elementos `<p>` (disposicion vacia) |
| `sample_bloque_xml_no_version` | Bloque sin elemento `<version>` (edge case) |
| `sample_bloque_xml_multi_class` | Art. 15 LIS con multiples clases CSS: `parrafo`, `parrafo_2`, `parrafo_3` |

Ejemplo de uso:

```python
def test_extracts_bloque_id(self, sample_bloque_xml):
    result = parse_bloque(sample_bloque_xml)
    assert result["id"] == "a29"
```

### Fixtures JSON

Respuestas JSON reales de la API del BOE.

| Fixture | Contenido |
|---------|-----------|
| `sample_metadatos_json` | Respuesta de `/metadatos` para BOE-A-2014-12328 (LIS) |
| `sample_indice_json` | Respuesta de `/texto/indice` con 6 bloques |

### Mock del BOEClient

```python
@pytest.fixture()
def mock_boe_client(sample_metadatos_json, sample_indice_json, sample_bloque_xml):
    client = AsyncMock()
    client.legislacion_metadatos.return_value = sample_metadatos_json
    client.legislacion_analisis.return_value = { ... }
    client.legislacion_indice.return_value = sample_indice_json["data"]["items"]
    client.legislacion_bloque.return_value = sample_bloque_xml
    client.legislacion_lista.return_value = { ... }
    client.sumario_boe.return_value = {"status": "OK", "data": {}}
    client.sumario_borme.return_value = {"status": "OK", "data": {}}
    client.datos_auxiliares.return_value = {"status": "OK", "data": []}
    return client
```

## Patrones de test

### Testar el XML parser (sin I/O)

Los tests del parser son sincronos y puros -- solo reciben XML y devuelven dicts:

```python
from normativa.xml_parser import parse_bloque, parse_indice

class TestParseBloqueNormal:
    def test_extracts_bloque_id(self, sample_bloque_xml):
        result = parse_bloque(sample_bloque_xml)
        assert result["id"] == "a29"

    def test_converts_articulo_class_to_heading(self, sample_bloque_xml):
        result = parse_bloque(sample_bloque_xml)
        assert "## Articulo 29. Tipo de gravamen." in result["texto_markdown"]

    def test_includes_indented_content(self, sample_bloque_xml):
        result = parse_bloque(sample_bloque_xml)
        assert "  No obstante" in result["texto_markdown"]
```

### Testar el registry (sin I/O)

El registry carga modulos Python, no hace HTTP. Los tests son sincronos:

```python
from normativa.registry import list_domains, load_domain, search_domains
from normativa.domains._base import DomainConfig

class TestLoadDomain:
    def test_fiscal_returns_domain_config(self):
        cfg = load_domain("fiscal")
        assert isinstance(cfg, DomainConfig)
        assert cfg.slug == "fiscal"

    def test_fiscal_has_4_leyes(self):
        cfg = load_domain("fiscal")
        assert len(cfg.leyes_clave) == 4

    def test_nonexistent_domain_raises(self):
        with pytest.raises(ValueError, match="Unknown domain"):
            load_domain("nonexistent_domain_xyz")
```

### Testar el cache (con `tmp_path`)

El cache necesita un fichero SQLite. Usa `tmp_path` de pytest para crear
una base de datos temporal que se limpia automaticamente:

```python
from normativa.cache import Cache

class TestGetOrFetch:
    async def test_stores_and_retrieves(self, tmp_path):
        db_path = tmp_path / "test.db"
        async with Cache(path=db_path) as cache:
            fetch_called = 0

            async def fetch():
                nonlocal fetch_called
                fetch_called += 1
                return {"titulo": "Ley de Prueba"}

            # Primera llamada: debe hacer fetch
            result = await cache.get_or_fetch("metadatos", "BOE-TEST-001", fetch)
            assert result == {"titulo": "Ley de Prueba"}
            assert fetch_called == 1

            # Segunda llamada: debe usar cache
            result2 = await cache.get_or_fetch("metadatos", "BOE-TEST-001", fetch)
            assert result2 == result
            assert fetch_called == 1  # fetch_fn NO se llama otra vez
```

Para testar expiracion, manipula directamente la DB:

```python
async def test_force_expire_by_manipulating_db(self, tmp_path):
    db_path = tmp_path / "test.db"
    async with Cache(path=db_path) as cache:
        # ... guardar un dato ...

        # Forzar expiracion
        past = (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat()
        await cache.db.execute(
            "UPDATE metadatos SET expires_at = ? WHERE key = ?",
            [past, "KEY-EXPIRE"],
        )
        await cache.db.commit()

        # Ahora debe hacer re-fetch
        result = await cache.get_or_fetch("metadatos", "KEY-EXPIRE", fetch, ttl_hours=1)
        assert fetch_count == 2
```

### Testar tools MCP (mock de `get_client`)

Las tools llaman a `get_client()` y `get_cache()` internamente. Usa
`unittest.mock.patch` para sustituirlos:

```python
from unittest.mock import AsyncMock, patch
from normativa.tools.search import buscar_por_dominio, buscar_legislacion

class TestBuscarPorDominio:
    async def test_returns_leyes_clave_for_fiscal(self):
        with patch("normativa.tools.search.get_client", new_callable=AsyncMock) as mock_gc:
            mock_client = AsyncMock()
            mock_client.legislacion_lista.side_effect = ConnectionError("mocked offline")
            mock_gc.return_value = mock_client

            result = await buscar_por_dominio(dominio="fiscal")

        assert "error" not in result
        assert result["dominio"] == "fiscal"
        assert "leyes_clave" in result
```

**Patron clave**: El mock de `get_client` fuerza un `ConnectionError` en la
API. Esto activa el fallback al registro local, que devuelve las leyes clave
del DomainConfig sin hacer HTTP.

Para testar con respuesta exitosa de la API:

```python
async def test_with_mock_api_success(self):
    with patch("normativa.tools.search.get_client", new_callable=AsyncMock) as mock_gc:
        mock_client = AsyncMock()
        mock_client.legislacion_lista.return_value = {
            "total": 1,
            "data": [
                {
                    "identificador": "BOE-A-2006-20764",
                    "titulo": "Ley 35/2006 del IRPF",
                    "rango": "Ley",
                    "fecha_publicacion": "20061129",
                    "estado_consolidacion": "Vigente",
                }
            ],
        }
        mock_gc.return_value = mock_client

        result = await buscar_legislacion(query="IRPF")

    assert result["total"] == 1
    assert result["resultados"][0]["boe_id"] == "BOE-A-2006-20764"
```

Para testar tools que usan cache, necesitas mockear ambos singletons:

```python
async def test_valid_response_parsed_correctly(self, sample_metadatos_json):
    with patch("normativa.tools.metadata.get_client", new_callable=AsyncMock) as mock_gc, \
         patch("normativa.tools.metadata.get_cache", new_callable=AsyncMock) as mock_cc:

        mock_client = AsyncMock()
        mock_client.legislacion_metadatos.return_value = sample_metadatos_json
        mock_gc.return_value = mock_client

        mock_cache = AsyncMock()
        async def passthrough_fetch(table, key, fn, **kwargs):
            return await fn()
        mock_cache.get_or_fetch.side_effect = passthrough_fetch
        mock_cc.return_value = mock_cache

        result = await obtener_metadatos("BOE-A-2014-12328")

    assert result["boe_id"] == "BOE-A-2014-12328"
```

El truco del `passthrough_fetch`: se configura `get_or_fetch` para que llame
directamente a la funcion `fetch_fn` sin cachear, evitando necesitar SQLite
en el test.

### Testar input invalido

Todas las tools deben devolver un dict con `"error"` cuando reciben input
invalido, sin lanzar excepciones:

```python
async def test_invalid_boe_id_returns_error(self):
    result = await obtener_metadatos("INVALID-ID-123")
    assert "error" in result
    assert "tool" in result
    assert result["tool"] == "obtener_metadatos"

async def test_empty_boe_id_returns_error(self):
    result = await obtener_metadatos("")
    assert "error" in result
```

## Escribir tests para nuevos dominios

Cuando creas un dominio nuevo, los tests existentes en `test_registry.py`
ya verifican automaticamente:

```python
def test_all_available_domains_load(self):
    for name in AVAILABLE_DOMAINS:
        cfg = load_domain(name)
        assert isinstance(cfg, DomainConfig)
        assert cfg.slug == name
```

Anade tests especificos si el dominio tiene EU refs o particularidades:

```python
def test_{slug}_has_eu_refs(self):
    cfg = load_domain("{slug}")
    eu_ref_count = sum(len(ley.eu_refs) for ley in cfg.leyes_clave.values())
    assert eu_ref_count >= 1

def test_{slug}_subtemas_have_leyes(self):
    cfg = load_domain("{slug}")
    for sub in cfg.subtemas:
        assert len(sub.leyes) >= 1, f"Subtema '{sub.slug}' sin leyes asignadas"
```

## Regla de oro

**Nunca hacer llamadas HTTP reales en tests.** Todo acceso a la API del BOE
se mockea con `AsyncMock` o `pytest-httpx`. Los tests deben ejecutarse offline
y en milisegundos.
