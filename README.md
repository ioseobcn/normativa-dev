# normativa-dev

**Legislacion espanola consolidada con dominios tematicos — MCP Server + API REST + CLI**

[![PyPI](https://img.shields.io/pypi/v/normativa)](https://pypi.org/project/normativa/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

Accede a toda la legislacion espanola a traves del [BOE](https://www.boe.es/) (Boletin Oficial del Estado) usando herramientas MCP optimizadas para LLMs, una API REST compatible con ChatGPT Actions, o una CLI directa.

**Web:** [normativa.dev](https://normativa.dev)

---

## Por que normativa

Los proyectos existentes son wrappers crudos de la API del BOE. `normativa` anade una **capa de inteligencia tematica** que:

- **Segmenta por dominios legales** — fiscal, laboral, mercantil, autonomos, proteccion de datos, digital, vivienda, medioambiental, consumo, penal, civil, administrativo
- **Pre-mapea leyes clave** con articulos importantes y sus IDs de bloque, evitando que el LLM tenga que buscar a ciegas
- **Optimiza el contexto** — nunca carga leyes completas; extrae articulos individuales bajo demanda (~12x mas eficiente en tokens)
- **Integra normativa europea** — referencias cruzadas con directivas y reglamentos EU (CELEX/ELI)
- **Tres transportes** — MCP (para Claude, Cursor, VS Code), HTTP REST (para ChatGPT, Codex, cualquier cliente), y CLI (para terminal)

---

## Instalacion

### Para usar con Claude Code (MCP)

Anade a `.mcp.json` en la raiz de tu proyecto:

```json
{
  "mcpServers": {
    "normativa": {
      "command": "uvx",
      "args": ["normativa"]
    }
  }
}
```

Reinicia Claude Code. Las 11 herramientas estaran disponibles automaticamente.

### Para usar con ChatGPT / GPTs (API HTTP)

```bash
# Instalar
pip install normativa

# Iniciar servidor HTTP
normativa serve --mode http --port 8787
```

Esto expone la API en `http://localhost:8787` con especificacion OpenAPI en `/api/openapi.json`. Para crear una GPT Action, importa esa URL como spec.

### Para usar como CLI

```bash
# Con uv (recomendado)
uvx normativa buscar "proteccion datos" --dominio digital

# Con pip
pip install normativa
normativa buscar "impuesto sociedades" --dominio fiscal
```

### Para usar con otros editores (Cursor, VS Code, Windsurf, OpenCode)

**Cursor** — En `Settings > MCP Servers`:

```json
{
  "normativa": {
    "command": "uvx",
    "args": ["normativa"]
  }
}
```

**VS Code + Continue/Copilot** — En `.vscode/mcp.json`:

```json
{
  "servers": {
    "normativa": {
      "command": "uvx",
      "args": ["normativa"]
    }
  }
}
```

**Windsurf** — En `.windsurf/mcp.json`:

```json
{
  "mcpServers": {
    "normativa": {
      "command": "uvx",
      "args": ["normativa"]
    }
  }
}
```

**OpenCode** — En `.opencode/mcp.json`:

```json
{
  "mcpServers": {
    "normativa": {
      "command": "uvx",
      "args": ["normativa"]
    }
  }
}
```

### Desde codigo Python

```python
from normativa.tools.search import buscar_legislacion, buscar_por_dominio
from normativa.tools.text import leer_articulo

# Buscar legislacion fiscal
resultado = await buscar_por_dominio("fiscal", subtema="iva")

# Leer un articulo concreto
articulo = await leer_articulo("BOE-A-2014-12328", "a29")
print(articulo["texto"])
```

---

## Plataformas compatibles

| Plataforma | Transporte | Configuracion |
|---|---|---|
| **Claude Code** | MCP (stdio) | `.mcp.json` |
| **Claude.ai web** | HTTP REST | URL del servidor |
| **ChatGPT / GPTs** | HTTP REST (OpenAPI) | Importar `/api/openapi.json` como Action |
| **Codex (OpenAI)** | HTTP REST | URL de la API |
| **Cursor** | MCP (stdio) | Settings > MCP Servers |
| **VS Code + Continue** | MCP (stdio) | `.vscode/mcp.json` |
| **VS Code + Copilot** | MCP (stdio) | `.vscode/mcp.json` |
| **Windsurf** | MCP (stdio) | `.windsurf/mcp.json` |
| **OpenCode** | MCP (stdio) | `.opencode/mcp.json` |
| **Terminal** | CLI | `pip install normativa` |
| **Python** | Libreria | `import normativa` |
| **Cualquier HTTP** | REST API | `curl http://host:8787/api/...` |

---

## Herramientas disponibles

| # | Herramienta | Endpoint HTTP | Descripcion |
|---|---|---|---|
| 1 | `listar_dominios` | `GET /api/dominios` | Lista dominios tematicos con leyes clave |
| 2 | `buscar_por_dominio` | `GET /api/buscar` | Busqueda inteligente por dominio juridico |
| 3 | `buscar_legislacion` | `GET /api/buscar/texto` | Busqueda texto libre en legislacion consolidada |
| 4 | `obtener_metadatos` | `GET /api/norma/{id}/metadatos` | Metadatos de una norma (titulo, fecha, estado) |
| 5 | `obtener_analisis` | `GET /api/norma/{id}/analisis` | Materias y referencias cruzadas |
| 6 | `leer_indice` | `GET /api/norma/{id}/indice` | Indice de articulos de una ley |
| 7 | `leer_articulo` | `GET /api/norma/{id}/articulo/{bloque}` | Texto de UN articulo en Markdown |
| 8 | `leer_articulos_rango` | `GET /api/norma/{id}/articulos` | Hasta 20 articulos consecutivos |
| 9 | `sumario_boe` | `GET /api/boe/sumario/{fecha}` | Sumario diario del BOE |
| 10 | `sumario_borme` | `GET /api/borme/sumario/{fecha}` | Sumario diario del BORME |
| 11 | `datos_auxiliares` | `GET /api/auxiliar/{tipo}` | Datos de referencia (materias, departamentos, rangos) |

---

## Dominios tematicos

| Dominio | Leyes clave | Subtemas | EU refs |
|---|---|---|---|
| `fiscal` | LIS, LIRPF, LIVA, LGT | IRPF, IVA, Impuesto Sociedades, General Tributaria | Directiva IVA, ATAD |
| `laboral` | ET, LGSS, LPRL | Contratos, despido, Seguridad Social, prevencion | -- |
| `mercantil` | LSC, CCom | Sociedades limitadas, anonimas, registro mercantil | -- |
| `autonomos` | LETA, LGSS-RETA | Alta, cotizacion, fiscalidad, facturacion | -- |
| `proteccion_datos` | LOPDGDD | Derechos afectado, obligaciones empresa, derechos digitales | RGPD |
| `digital` | LSSI | Comercio electronico, cookies, aviso legal | Dir. eCommerce, ePrivacy |
| `vivienda` | Ley Vivienda, LAU | Alquiler, zonas tensionadas, desahucio | -- |
| `medioambiental` | LRMA, Ley Cambio Climatico | Evaluacion ambiental, residuos, emisiones | Directiva EIA |
| `penal` | CP, LECrim | Delitos, penas, procedimiento penal | -- |
| `civil` | CC, LEC | Obligaciones, contratos, familia, sucesiones | -- |
| `administrativo` | LPAC, LRJSP | Procedimiento administrativo, regimen juridico | -- |
| `consumo` | LGDCU | Garantias, reclamaciones, comercio electronico | Directiva Consumidores |

---

## API REST

Inicia el servidor:

```bash
normativa serve --mode http --port 8787
```

Ejemplos con curl:

```bash
# Listar dominios tematicos
curl http://localhost:8787/api/dominios

# Buscar por dominio fiscal
curl "http://localhost:8787/api/buscar?dominio=fiscal&subtema=iva"

# Busqueda texto libre
curl "http://localhost:8787/api/buscar/texto?q=proteccion+datos&limit=5"

# Metadatos de una norma
curl http://localhost:8787/api/norma/BOE-A-2014-12328/metadatos

# Leer un articulo concreto
curl http://localhost:8787/api/norma/BOE-A-2014-12328/articulo/a29

# Indice de una norma
curl http://localhost:8787/api/norma/BOE-A-2014-12328/indice

# Rango de articulos
curl "http://localhost:8787/api/norma/BOE-A-2014-12328/articulos?desde=a1&hasta=a5"

# Sumario BOE de hoy
curl http://localhost:8787/api/boe/sumario/2026-04-05

# Sumario BORME
curl http://localhost:8787/api/borme/sumario/2026-04-05

# Datos auxiliares (materias)
curl "http://localhost:8787/api/auxiliar/materias?buscar=tributario"

# Especificacion OpenAPI (para ChatGPT Actions)
curl http://localhost:8787/api/openapi.json
```

Documentacion interactiva en `http://localhost:8787/docs` (Swagger UI).

---

## Equipo de agentes

`normativa` incluye 11 agentes para Claude Code (6 legales + 5 desarrollo):

```
Fase 1 (paralelo):  investigador-legal + monitor-cambios
Fase 2:             extractor-articulos
Fase 3 (paralelo):  analista-dominio + verificador-cumplimiento
Fase 4:             redactor-informes
```

Los agentes se comunican via archivos en `handoff/`, pasando **referencias** (BOE IDs + bloque IDs) en lugar de texto completo. Esto mantiene el consumo de tokens ~12x mas eficiente que cargar leyes enteras.

---

## Arquitectura

```
+---------------------------------------------------------+
|  CAPA 5: HTTP REST API (FastAPI + OpenAPI auto)         |
|  GET /api/buscar, /api/norma/{id}/articulo/{bloque}...  |
+---------------------------------------------------------+
|  CAPA 4: Agent Team (11 agentes .claude/agents/)        |
|  investigador -> extractor -> analista -> redactor       |
+---------------------------------------------------------+
|  CAPA 3: Skills (10 packs .claude/skills/)              |
|  Conocimiento de dominio lazy-loaded                    |
+---------------------------------------------------------+
|  CAPA 2: MCP Server (11 tools FastMCP)                  |
|  Domain Registry + Cache SQLite + XML Parser            |
+---------------------------------------------------------+
|  CAPA 1: BOE API Client (httpx async)                   |
|  /legislacion-consolidada + /sumario + /auxiliar         |
+---------------------------------------------------------+
```

La capa HTTP (5) envuelve las mismas funciones de herramientas de la capa MCP (2), reutilizando toda la logica sin duplicar codigo.

---

## Desarrollo

```bash
# Clonar y configurar
git clone https://github.com/ioseobcn/normativa-dev.git
cd normativa-dev
uv sync

# Tests
uv run pytest -v

# Documentacion local
uv run mkdocs serve

# CLI
uv run normativa buscar "despido" --dominio laboral

# Servidor HTTP en desarrollo
uv run normativa serve --mode http --port 8787
```

Consulta la [guia de contribucion](docs/contributing.md) y la [documentacion de desarrollo](docs/dev/index.md) para mas detalles.

---

## Fuente de datos

Toda la legislacion proviene de la [API de datos abiertos del BOE](https://www.boe.es/datosabiertos/) (Agencia Estatal Boletin Oficial del Estado). Los datos son publicos y de dominio publico.

## Aviso legal

Este software tiene caracter informativo y **no constituye asesoramiento legal**. Consulte con un profesional antes de tomar decisiones basadas en los resultados obtenidos.

## Licencia

[MIT](LICENSE) — [InnovaOrigen](https://innovaorigen.io) 2026
