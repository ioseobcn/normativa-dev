# normativa

**Legislacion espanola consolidada con dominios tematicos — MCP Server + CLI**

[![PyPI](https://img.shields.io/pypi/v/normativa)](https://pypi.org/project/normativa/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

Accede a la legislacion espanola a traves del [BOE](https://www.boe.es/) (Boletin Oficial del Estado) usando herramientas MCP optimizadas para LLMs o una CLI directa.

**Web:** [normativa.dev](https://normativa.dev)

## Por que normativa

Los proyectos existentes son wrappers crudos de la API del BOE. `normativa` anade una **capa de inteligencia tematica** que:

- **Segmenta por dominios legales** — fiscal, laboral, mercantil, autonomos, proteccion de datos, digital, vivienda
- **Pre-mapea leyes clave** con articulos importantes y sus IDs de bloque
- **Optimiza el contexto** — nunca carga leyes completas; extrae articulos individuales bajo demanda
- **Incluye un equipo de 6 agentes** especializados con pipeline de investigacion legal

## Instalacion

```bash
# Con uv (recomendado)
uvx normativa

# Con pip
pip install normativa
```

## Uso como MCP Server

Anade a tu configuracion de Claude Code (`.mcp.json`):

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

| Herramienta | Descripcion |
|-------------|-------------|
| `buscar_por_dominio` | Busca legislacion por dominio tematico (fiscal, laboral...) |
| `buscar_legislacion` | Busqueda texto libre en legislacion consolidada |
| `obtener_metadatos` | Metadatos de una norma (titulo, fecha, estado) |
| `obtener_analisis` | Materias y referencias normativas |
| `leer_indice` | Indice de articulos de una ley |
| `leer_articulo` | Texto de UN articulo en markdown |
| `leer_articulos_rango` | Hasta 10 articulos consecutivos |
| `sumario_boe` | Sumario diario del BOE, filtrable por dominio |
| `sumario_borme` | Sumario diario del BORME |
| `listar_dominios` | Lista dominios tematicos disponibles |
| `datos_auxiliares` | Datos de referencia (materias, departamentos, rangos) |

## Uso como CLI

```bash
# Buscar legislacion por dominio
normativa buscar "impuesto sociedades" --dominio fiscal

# Ver leyes de un dominio
normativa dominio fiscal

# Leer un articulo especifico
normativa articulo BOE-A-2014-12328 a29

# Ver indice de una ley
normativa indice BOE-A-2014-12328

# Sumario del BOE de hoy
normativa sumario

# Iniciar servidor MCP
normativa serve
```

## Dominios tematicos

| Dominio | Leyes clave | Subtemas |
|---------|-------------|----------|
| `fiscal` | LIS, LIRPF, LIVA, LGT | IRPF, IVA, Impuesto Sociedades, General Tributaria |
| `laboral` | ET, LGSS, LPRL | Contratos, despido, Seguridad Social, prevencion |
| `mercantil` | LSC, CCom | Sociedades limitadas, anonimas, registro mercantil |
| `autonomos` | LETA, LGSS-RETA | Alta, cotizacion, fiscalidad, facturacion |
| `proteccion_datos` | LOPDGDD | Derechos afectado, obligaciones empresa, derechos digitales |
| `digital` | LSSI | Comercio electronico, cookies, aviso legal |
| `vivienda` | Ley Vivienda, LAU | Alquiler, zonas tensionadas, desahucio |

## Equipo de agentes

`normativa` incluye 6 agentes especializados para Claude Code que trabajan en pipeline:

```
Fase 1 (paralelo):  investigador-legal + monitor-cambios
Fase 2:             extractor-articulos
Fase 3 (paralelo):  analista-dominio + verificador-cumplimiento
Fase 4:             redactor-informes
```

Los agentes se comunican via archivos en `handoff/`, pasando **referencias** (BOE IDs + bloque IDs) en lugar de texto completo. Esto mantiene el consumo de tokens ~12x mas eficiente que cargar leyes enteras.

## Arquitectura

```
+---------------------------------------------------+
|  CAPA 4: Agent Team (6 agentes .claude/agents/)   |
|  investigador > extractor > analista > redactor    |
+---------------------------------------------------+
|  CAPA 3: Skills (8 packs .claude/skills/)          |
|  Conocimiento de dominio lazy-loaded               |
+---------------------------------------------------+
|  CAPA 2: MCP Server (11 tools FastMCP)             |
|  Domain Registry + Cache SQLite + XML Parser       |
+---------------------------------------------------+
|  CAPA 1: BOE API Client (httpx async)              |
|  /legislacion-consolidada + /sumario + /auxiliar   |
+---------------------------------------------------+
```

## Fuente de datos

Toda la legislacion proviene de la [API de datos abiertos del BOE](https://www.boe.es/datosabiertos/) (Agencia Estatal Boletin Oficial del Estado). Los datos son publicos y de dominio publico.

## Aviso legal

Este software tiene caracter informativo y **no constituye asesoramiento legal**. Consulte con un profesional antes de tomar decisiones basadas en los resultados obtenidos.

## Licencia

[MIT](LICENSE) — [InnovaOrigen](https://innovaorigen.io) 2026
