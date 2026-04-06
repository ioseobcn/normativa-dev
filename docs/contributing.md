# Contribuir

## Setup de desarrollo

```bash
git clone https://github.com/ioseobcn/normativa.git
cd normativa
uv sync
```

## Como anadir un nuevo dominio

### 1. Crear el modulo de dominio

Crea `src/normativa/domains/<nombre>.py`:

```python
"""Dominio <nombre> — descripcion breve."""

from normativa.domains._base import DomainConfig, EURef, LeyRef, Subtema

DOMAIN = DomainConfig(
    slug="<nombre>",
    nombre="Nombre visible del dominio",
    descripcion="Descripcion completa del dominio.",
    leyes_clave={
        "BOE-A-YYYY-NNNNN": LeyRef(
            boe_id="BOE-A-YYYY-NNNNN",
            nombre_corto="Nombre corto",
            titulo_oficial="Titulo oficial completo",
            rango="Ley",
            articulos_clave={
                "a1": "Descripcion del articulo 1",
            },
            eu_refs=[],  # Anadir EURef si transpone/implementa directiva UE
        ),
    },
    subtemas=[
        Subtema(
            slug="subtema_1",
            nombre="Subtema 1",
            descripcion="Descripcion del subtema.",
            leyes=["BOE-A-YYYY-NNNNN"],
            terminos_busqueda=["termino1", "termino2"],
            casos_uso=["Caso de uso 1", "Caso de uso 2"],
        ),
    ],
    materias_boe=[],  # Codigos de materia del BOE
    terminos_busqueda=["termino1", "termino2"],
    casos_uso={
        "caso_1": "Descripcion del caso de uso",
    },
)
```

### 2. Registrar el dominio

Anade el slug a `AVAILABLE_DOMAINS` en `src/normativa/domains/__init__.py`:

```python
AVAILABLE_DOMAINS: list[str] = [
    "fiscal",
    "laboral",
    # ...
    "<nombre>",  # <-- nuevo
]
```

### 3. Verificar con la API

Comprueba que los BOE IDs son validos:

```bash
# Verificar metadatos
normativa articulo BOE-A-YYYY-NNNNN a1

# Verificar indice
normativa indice BOE-A-YYYY-NNNNN
```

### 4. Escribir tests

Crea `tests/test_domain_<nombre>.py`:

```python
"""Tests para dominio <nombre>."""

from normativa.domains.<nombre> import DOMAIN
from normativa.domains._base import DomainConfig


def test_domain_config():
    assert isinstance(DOMAIN, DomainConfig)
    assert DOMAIN.slug == "<nombre>"
    assert len(DOMAIN.leyes_clave) > 0


def test_articulos_clave():
    for boe_id, ley in DOMAIN.leyes_clave.items():
        assert boe_id.startswith("BOE-")
        assert len(ley.articulos_clave) > 0
```

### 5. Documentar

Crea `docs/domains/<nombre>.md` y anade la entrada al `nav` en `mkdocs.yml`.

## Como anadir referencias UE

En el `LeyRef` de la ley que transpone la directiva/reglamento:

```python
eu_refs=[
    EURef(
        celex="32016R0679",          # Numero CELEX
        titulo="RGPD",               # Nombre corto
        tipo="reglamento",           # reglamento, directiva, decision
        eli_url="http://data.europa.eu/eli/reg/2016/679/oj",
        relacion="transpone",        # transpone, implementa, complementa
    ),
],
```

Busca el numero CELEX en [EUR-Lex](https://eur-lex.europa.eu/).

## Como escribir tests

```bash
# Ejecutar todos los tests
uv run pytest -v

# Ejecutar tests de un modulo
uv run pytest tests/test_domain_fiscal.py -v

# Ejecutar un test concreto
uv run pytest tests/test_domain_fiscal.py::test_domain_config -v
```

Los tests de herramientas que llaman a la API del BOE deben mockearse con `pytest-httpx`:

```python
import pytest
from normativa.tools.search import buscar_legislacion


@pytest.mark.asyncio
async def test_buscar_legislacion(httpx_mock):
    httpx_mock.add_response(json={"data": [], "total": 0})
    result = await buscar_legislacion("test")
    assert "resultados" in result
```

## Estilo de codigo

- Python 3.11+
- Type hints en todas las funciones publicas
- Docstrings en espanol (sin tildes en el codigo fuente)
- `from __future__ import annotations` en todos los modulos
- Funciones async para todas las herramientas MCP
- Tests con `pytest` y `pytest-asyncio`
