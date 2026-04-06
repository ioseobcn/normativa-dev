# Inicio rapido

## Instalacion

### Con uv (recomendado)

```bash
uvx normativa
```

### Con pip

```bash
pip install normativa
```

### Desde el codigo fuente

```bash
git clone https://github.com/ioseobcn/normativa-dev.git
cd normativa
uv sync
uv run normativa --help
```

## Configurar MCP en Claude Code

Crea o edita `.mcp.json` en la raiz de tu proyecto:

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

## Primera consulta: buscar por dominio

La herramienta diferenciadora de `normativa` es `buscar_por_dominio`. En vez de construir queries complejas, indica el dominio juridico:

```python
buscar_por_dominio("fiscal", subtema="iva")
```

Esto genera automaticamente los terminos de busqueda adecuados para la API del BOE y devuelve legislacion relevante con las leyes clave pre-mapeadas.

## Leer un articulo concreto

Usa `leer_articulo` para obtener el texto exacto de un articulo en Markdown:

```python
leer_articulo("BOE-A-2014-12328", "a29")
```

Resultado: el articulo 29 de la Ley del Impuesto sobre Sociedades (tipo de gravamen).

!!! tip "Patron recomendado"
    1. `leer_indice(boe_id)` -- ver la estructura de la norma
    2. `leer_articulo(boe_id, bloque_id)` -- leer UN articulo concreto
    3. `leer_articulos_rango(boe_id, desde, hasta)` -- solo si necesitas un bloque consecutivo

## Usar la CLI

```bash
# Buscar legislacion por dominio
normativa buscar "impuesto sociedades" --dominio fiscal

# Ver leyes de un dominio
normativa dominio fiscal

# Leer un articulo
normativa articulo BOE-A-2014-12328 a29

# Ver indice de una ley
normativa indice BOE-A-2014-12328

# Sumario del BOE de hoy
normativa sumario

# Sumario de una fecha concreta
normativa sumario 2026-04-01
```

## Siguiente paso

- [Referencia completa de la CLI](cli.md)
- [Configuracion avanzada del servidor MCP](mcp.md)
- [Vision general de los dominios tematicos](../domains/index.md)
