# MCP Server

`normativa` expone 11 herramientas via el protocolo MCP (Model Context Protocol) usando FastMCP.

## Configuracion

### Claude Code

Crea `.mcp.json` en la raiz de tu proyecto:

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

### Cursor

En `Settings > MCP Servers`, anade:

```json
{
  "normativa": {
    "command": "uvx",
    "args": ["normativa"]
  }
}
```

### VS Code (Copilot)

En `.vscode/mcp.json`:

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

### Instalacion local (sin uvx)

Si prefieres no usar `uvx`:

```json
{
  "mcpServers": {
    "normativa": {
      "command": "python",
      "args": ["-m", "normativa"]
    }
  }
}
```

Asegurate de que `normativa` esta instalado en el entorno Python que usa el `command`.

## Herramientas disponibles

| Herramienta | Descripcion |
|---|---|
| `buscar_legislacion` | Busqueda texto libre en legislacion consolidada |
| `buscar_por_dominio` | Busca por dominio tematico (fiscal, laboral...) |
| `obtener_metadatos` | Metadatos de una norma (titulo, fecha, estado) |
| `obtener_analisis` | Materias y referencias normativas |
| `leer_indice` | Indice de articulos de una ley |
| `leer_articulo` | Texto de UN articulo en Markdown |
| `leer_articulos_rango` | Hasta 10 articulos consecutivos |
| `sumario_boe` | Sumario diario del BOE, filtrable por dominio |
| `sumario_borme` | Sumario diario del BORME |
| `listar_dominios` | Lista dominios tematicos disponibles |
| `datos_auxiliares` | Datos de referencia (materias, departamentos, rangos) |

## Ejemplo de conversacion

**Usuario:** Necesito saber el tipo de gravamen del Impuesto de Sociedades.

**Asistente (usa herramientas):**

1. `buscar_por_dominio("fiscal", subtema="impuesto_sociedades")` -- identifica la Ley IS (BOE-A-2014-12328) y que el articulo clave es `a29`
2. `leer_articulo("BOE-A-2014-12328", "a29")` -- lee el texto del articulo 29

**Resultado:** El tipo general es del 25% (art. 29.1 LIS), con tipos reducidos para entidades de nueva creacion (15%), entidades sin animo de lucro, cooperativas, etc.

## Patron de uso eficiente

El diseno de `normativa` optimiza el consumo de contexto:

1. **Nunca carga leyes completas** -- usa `leer_articulo` para articulos individuales
2. **Pre-mapea articulos clave** -- cada dominio tiene los articulos mas consultados identificados
3. **Fallback local** -- si la API del BOE no esta disponible, devuelve leyes del registro interno
4. **Cache SQLite** -- evita llamadas repetidas a la API

!!! warning "Limite de la API del BOE"
    La busqueda por texto (`buscar_legislacion`) esta limitada a 500 resultados por la API. Para busquedas mas especificas, usa `buscar_por_dominio` que pre-filtra con terminos optimizados.
