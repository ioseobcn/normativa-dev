# CLI

`normativa` incluye una CLI completa para consulta de legislacion desde terminal.

```bash
normativa --help
normativa --version
```

## Comandos

### `buscar` -- Busqueda de legislacion

Busca legislacion por texto libre, opcionalmente filtrada por dominio.

```bash
# Busqueda general
normativa buscar "proteccion datos personales"

# Filtrar por dominio
normativa buscar "despido improcedente" --dominio laboral

# Limitar resultados
normativa buscar "IVA tipo reducido" -n 5

# Filtrar por rango normativo
normativa buscar "impuesto" --rango "Ley"

# Salida JSON
normativa buscar "arrendamiento urbano" --json
```

| Opcion | Corto | Descripcion |
|---|---|---|
| `--dominio` | `-d` | Filtrar por dominio tematico |
| `--limit` | `-n` | Maximo de resultados (default: 10) |
| `--rango` | | Tipo de norma (Ley, Real Decreto...) |
| `--json` | | Salida en formato JSON |

### `dominio` -- Dominios tematicos

Lista dominios disponibles o busca dentro de un dominio concreto.

```bash
# Listar todos los dominios
normativa dominio

# Ver leyes de un dominio
normativa dominio fiscal

# Filtrar por subtema
normativa dominio laboral --subtema despido
```

| Opcion | Corto | Descripcion |
|---|---|---|
| `--subtema` | `-s` | Filtrar por subtema del dominio |

### `articulo` -- Leer un articulo

Lee el texto de un articulo concreto de una norma consolidada.

```bash
# Leer articulo 29 de la Ley del Impuesto sobre Sociedades
normativa articulo BOE-A-2014-12328 a29

# Salida JSON
normativa articulo BOE-A-2006-20764 a7 --json
```

| Argumento | Descripcion |
|---|---|
| `BOE_ID` | Identificador BOE de la norma |
| `BLOQUE_ID` | ID del bloque/articulo (ej: `a29`) |

### `indice` -- Indice de una norma

Muestra la tabla de contenidos de una norma consolidada.

```bash
# Ver indice de la Ley IRPF
normativa indice BOE-A-2006-20764

# En formato JSON
normativa indice BOE-A-2014-12328 --json
```

### `sumario` -- Sumario diario del BOE

Muestra las disposiciones publicadas en el BOE para una fecha.

```bash
# Sumario de hoy
normativa sumario

# Sumario de una fecha concreta
normativa sumario 2026-04-01

# Filtrar por dominio
normativa sumario --dominio fiscal

# Filtrar por seccion del BOE
normativa sumario --seccion I

# Salida JSON
normativa sumario --json
```

| Opcion | Corto | Descripcion |
|---|---|---|
| `--dominio` | `-d` | Filtrar por dominio tematico |
| `--seccion` | `-s` | Filtrar por seccion BOE (I, II, III, IV, V) |
| `--json` | | Salida en formato JSON |

Formatos de fecha aceptados: `YYYY-MM-DD`, `DD/MM/YYYY`, `YYYYMMDD`.

### `serve` -- Iniciar servidor MCP

Inicia el servidor MCP en modo stdio para uso con Claude Code, Cursor u otros clientes MCP.

```bash
normativa serve
```

Este comando es el que ejecuta internamente la configuracion MCP (`"command": "uvx", "args": ["normativa"]` equivale a `normativa serve`).
