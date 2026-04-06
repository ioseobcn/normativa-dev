# normativa-dev

**Legislación española consolidada con dominios temáticos — MCP Server + CLI**

[![PyPI](https://img.shields.io/pypi/v/normativa)](https://pypi.org/project/normativa/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

Accede a la legislación española a través del [BOE](https://www.boe.es/) (Boletín Oficial del Estado) usando herramientas MCP optimizadas para LLMs o una CLI directa.

**Web:** [normativa.dev](https://normativa.dev)

## Por qué normativa

Los proyectos existentes son wrappers crudos de la API del BOE. `normativa` añade una **capa de inteligencia temática** que:

- **Segmenta por dominios legales** — fiscal, laboral, mercantil, autónomos, protección de datos, digital, vivienda
- **Pre-mapea leyes clave** con artículos importantes y sus IDs de bloque
- **Optimiza el contexto** — nunca carga leyes completas; extrae artículos individuales bajo demanda
- **Incluye un equipo de 6 agentes** especializados con pipeline de investigación legal
- **Integra normativa europea** — referencias cruzadas con directivas y reglamentos EU (CELEX/ELI)

## Instalación

```bash
# Con uv (recomendado)
uvx normativa

# Con pip
pip install normativa
```

## Uso como MCP Server

Añade a tu configuración de Claude Code (`.mcp.json`):

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

Esto te da acceso a 11 herramientas:

| Herramienta | Descripción |
|-------------|-------------|
| `buscar_por_dominio` | Busca legislación por dominio temático (fiscal, laboral...) |
| `buscar_legislacion` | Búsqueda texto libre en legislación consolidada |
| `obtener_metadatos` | Metadatos de una norma (título, fecha, estado) |
| `obtener_analisis` | Materias y referencias normativas |
| `leer_indice` | Índice de artículos de una ley |
| `leer_articulo` | Texto de UN artículo en markdown |
| `leer_articulos_rango` | Hasta 10 artículos consecutivos |
| `sumario_boe` | Sumario diario del BOE, filtrable por dominio |
| `sumario_borme` | Sumario diario del BORME |
| `listar_dominios` | Lista dominios temáticos disponibles |
| `datos_auxiliares` | Datos de referencia (materias, departamentos, rangos) |

## Uso como CLI

```bash
# Buscar legislación por dominio
normativa buscar "impuesto sociedades" --dominio fiscal

# Ver leyes de un dominio
normativa dominio fiscal

# Leer un artículo específico
normativa articulo BOE-A-2014-12328 a29

# Ver índice de una ley
normativa indice BOE-A-2014-12328

# Sumario del BOE de hoy
normativa sumario

# Iniciar servidor MCP
normativa serve
```

## Dominios temáticos

| Dominio | Leyes clave | Subtemas | EU refs |
|---------|-------------|----------|---------|
| `fiscal` | LIS, LIRPF, LIVA, LGT | IRPF, IVA, Impuesto Sociedades, General Tributaria | Directiva IVA, ATAD |
| `laboral` | ET, LGSS, LPRL | Contratos, despido, Seguridad Social, prevención | — |
| `mercantil` | LSC, CCom | Sociedades limitadas, anónimas, registro mercantil | — |
| `autonomos` | LETA, LGSS-RETA | Alta, cotización, fiscalidad, facturación | — |
| `proteccion_datos` | LOPDGDD | Derechos afectado, obligaciones empresa, derechos digitales | RGPD |
| `digital` | LSSI | Comercio electrónico, cookies, aviso legal | Dir. eCommerce, ePrivacy |
| `vivienda` | Ley Vivienda, LAU | Alquiler, zonas tensionadas, desahucio | — |

## Equipo de agentes

`normativa` incluye 11 agentes para Claude Code (6 legales + 5 desarrollo):

```
Fase 1 (paralelo):  investigador-legal + monitor-cambios
Fase 2:             extractor-articulos
Fase 3 (paralelo):  analista-dominio + verificador-cumplimiento
Fase 4:             redactor-informes
```

Los agentes se comunican vía archivos en `handoff/`, pasando **referencias** (BOE IDs + bloque IDs) en lugar de texto completo. Esto mantiene el consumo de tokens ~12x más eficiente que cargar leyes enteras.

## Arquitectura

```
┌───────────────────────────────────────────────────┐
│  CAPA 4: Agent Team (11 agentes .claude/agents/)  │
│  investigador → extractor → analista → redactor   │
├───────────────────────────────────────────────────┤
│  CAPA 3: Skills (10 packs .claude/skills/)        │
│  Conocimiento de dominio lazy-loaded              │
├───────────────────────────────────────────────────┤
│  CAPA 2: MCP Server (11 tools FastMCP)            │
│  Domain Registry + Caché SQLite + XML Parser      │
├───────────────────────────────────────────────────┤
│  CAPA 1: BOE API Client (httpx async)             │
│  /legislacion-consolidada + /sumario + /auxiliar  │
└───────────────────────────────────────────────────┘
```

## Desarrollo

```bash
# Clonar y configurar
git clone https://github.com/ioseobcn/normativa-dev.git
cd normativa-dev
uv sync

# Tests
uv run pytest -v

# Documentación local
uv run mkdocs serve

# CLI
uv run normativa buscar "despido" --dominio laboral
```

Consulta la [guía de contribución](docs/contributing.md) y la [documentación de desarrollo](docs/dev/index.md) para más detalles.

## Fuente de datos

Toda la legislación proviene de la [API de datos abiertos del BOE](https://www.boe.es/datosabiertos/) (Agencia Estatal Boletín Oficial del Estado). Los datos son públicos y de dominio público.

## Aviso legal

Este software tiene carácter informativo y **no constituye asesoramiento legal**. Consulte con un profesional antes de tomar decisiones basadas en los resultados obtenidos.

## Licencia

[MIT](LICENSE) — [InnovaOrigen](https://innovaorigen.io) 2026
