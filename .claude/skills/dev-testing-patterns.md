# Skill: Testing Patterns

Patrones y ejemplos para escribir tests en normativa.

## Setup

```bash
uv sync --group dev                # Instalar dependencias de test
uv run pytest -v                   # Ejecutar todos los tests
uv run pytest -k "test_fiscal"     # Filtrar por nombre
uv run pytest --tb=short           # Traceback corto
```

## Configuracion (pyproject.toml)

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"

[dependency-groups]
dev = ["pytest>=8.0", "pytest-asyncio>=0.23", "pytest-httpx>=0.30"]
```

Con `asyncio_mode = "auto"`, las funciones async se detectan automaticamente sin decorador.

## Patron: test de XML parser

```python
from normativa.xml_parser import parse_bloque

def test_parse_bloque_normal():
    xml = '''<bloque id="a29" tipo="precepto" titulo="Articulo 29.">
        <version id_norma="BOE-A-2014-12328" fecha_publicacion="20141128" fecha_vigencia="20150101">
            <p class="articulo">Articulo 29. Tipo de gravamen.</p>
            <p class="parrafo">El tipo general sera del 25 por ciento.</p>
        </version>
    </bloque>'''
    result = parse_bloque(xml)
    assert result["id"] == "a29"
    assert result["tipo"] == "precepto"
    assert "25 por ciento" in result["texto_markdown"]
```

## Patron: test de registry (sin I/O)

```python
from normativa.registry import list_domains, load_domain, search_domains

def test_list_domains_count():
    domains = list_domains()
    assert len(domains) >= 7

def test_load_fiscal():
    cfg = load_domain("fiscal")
    assert cfg.slug == "fiscal"
    assert len(cfg.leyes_clave) == 4

def test_search_cross_domain():
    results = search_domains("RGPD cookies")
    slugs = [r["slug"] for r in results]
    assert "proteccion_datos" in slugs
    assert "digital" in slugs
```

## Patron: test de cache (con tmp_path)

```python
import asyncio
from normativa.cache import Cache

async def test_cache_stores_and_retrieves(tmp_path):
    db_path = tmp_path / "test.db"
    async with Cache(path=db_path) as cache:
        result = await cache.get_or_fetch(
            "metadatos", "BOE-TEST-001",
            fetch_fn=lambda: asyncio.coroutine(lambda: {"titulo": "Test"})()
        )
        assert result == {"titulo": "Test"}
        assert db_path.exists()
```

## Patron: mock del BOEClient (sin HTTP)

```python
from unittest.mock import AsyncMock

def mock_boe_client(metadatos_response, indice_response):
    client = AsyncMock()
    client.legislacion_metadatos.return_value = metadatos_response
    client.legislacion_indice.return_value = indice_response
    client.legislacion_lista.return_value = {"data": [], "total": 0}
    client.legislacion_bloque.return_value = "<bloque/>"
    return client
```

## Patron: test de tools MCP

```python
async def test_buscar_por_dominio_fiscal():
    result = await buscar_por_dominio(dominio="fiscal")
    assert "error" not in result
    assert result["dominio"] == "fiscal"
    assert "leyes_clave" in result
```

Los tools devuelven dicts. Errores: `{"error": "...", "tool": "nombre"}`.
Nunca deben lanzar excepciones al MCP.

## Patron: test de tools con invalid input

```python
async def test_obtener_metadatos_invalid_id():
    result = await obtener_metadatos("INVALID-ID")
    assert "error" in result
    assert "tool" in result
```

## Reglas

- Nunca hacer llamadas HTTP reales en tests
- Usar `tmp_path` para bases de datos temporales
- Fixtures en conftest.py, compartidas entre test files
- Un test = una asercion principal (pueden tener asserts auxiliares)
- Nombres descriptivos: `test_{que}_{condicion}_{esperado}`
