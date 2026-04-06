# Inicio rapido

`normativa` funciona en cualquier plataforma que soporte MCP o HTTP. Elige tu entorno y sigue los pasos.

---

## Claude Code

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

Reinicia Claude Code. Las 11 herramientas estaran disponibles automaticamente. Prueba con:

> "Busca legislacion sobre proteccion de datos en el dominio digital"

---

## Cursor

En `Settings > MCP Servers`, anade un nuevo servidor:

```json
{
  "normativa": {
    "command": "uvx",
    "args": ["normativa"]
  }
}
```

Reinicia Cursor para activar las herramientas.

---

## VS Code + Continue

Crea o edita `.vscode/mcp.json` en tu proyecto:

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

Continue detectara las herramientas de normativa automaticamente.

---

## VS Code + Copilot

Misma configuracion que Continue. Crea `.vscode/mcp.json`:

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

---

## Windsurf

Crea `.windsurf/mcp.json` en la raiz de tu proyecto:

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

---

## OpenCode

Crea `.opencode/mcp.json` en la raiz de tu proyecto:

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

---

## ChatGPT / GPTs (API HTTP)

Para usar normativa como Action de un GPT personalizado:

1. **Instala e inicia el servidor HTTP:**

    ```bash
    pip install normativa
    normativa serve --mode http --port 8787
    ```

2. **Expone el servidor** (si es necesario) con un tunel o despliega en la nube.

3. **En ChatGPT**, ve a "Configurar GPT" > "Acciones" > "Crear nueva accion".

4. **Importa la especificacion OpenAPI** desde:

    ```
    http://tu-servidor:8787/api/openapi.json
    ```

5. ChatGPT detectara automaticamente los 11 endpoints y podra usarlos.

Para mas detalles, consulta la [guia de la API HTTP](http-api.md).

---

## Terminal / CLI

```bash
# Instalar
pip install normativa
# o con uv
uvx normativa --help

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

# Sumario de una fecha concreta
normativa sumario 2026-04-01

# Iniciar servidor MCP
normativa serve

# Iniciar servidor HTTP
normativa serve --mode http --port 8787
```

---

## Libreria Python

Todas las herramientas son funciones `async` que puedes importar directamente:

```python
import asyncio
from normativa.tools.search import buscar_legislacion, buscar_por_dominio
from normativa.tools.text import leer_indice, leer_articulo
from normativa.tools.domain import listar_dominios

async def main():
    # Listar dominios disponibles
    dominios = await listar_dominios()
    print(dominios["total"], "dominios")

    # Buscar por dominio
    resultado = await buscar_por_dominio("fiscal", subtema="iva")
    for r in resultado.get("resultados", []):
        print(r["boe_id"], r["titulo"])

    # Leer un articulo
    art = await leer_articulo("BOE-A-2014-12328", "a29")
    print(art["texto"])

asyncio.run(main())
```

---

## API HTTP directa

```bash
# Iniciar servidor
normativa serve --mode http --port 8787

# Consultar desde otro terminal
curl http://localhost:8787/api/dominios
curl "http://localhost:8787/api/buscar?dominio=fiscal&subtema=iva"
curl http://localhost:8787/api/norma/BOE-A-2014-12328/articulo/a29
```

Documentacion interactiva en `http://localhost:8787/docs`.

---

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

---

## Siguiente paso

- [Referencia completa de la CLI](cli.md)
- [Configuracion del servidor MCP](mcp.md)
- [API HTTP completa](http-api.md)
- [Vision general de los dominios tematicos](../domains/index.md)
