# normativa

**Legislacion espanola consolidada con dominios tematicos**

`normativa` es un servidor MCP + CLI que da acceso a la legislacion espanola consolidada a traves de la API abierta del BOE (Boletin Oficial del Estado), con una capa de inteligencia tematica que segmenta la normativa por dominios juridicos.

---

## Caracteristicas

| Caracteristica | Detalle |
|---|---|
| **7 dominios tematicos** | Fiscal, Laboral, Mercantil, Autonomos, Proteccion de datos, Digital, Vivienda |
| **11 herramientas MCP** | Busqueda, lectura de articulos, sumarios, metadatos, analisis |
| **9 agentes especializados** | 6 legales + 3 de desarrollo, pipeline de investigacion |
| **17 leyes mapeadas** | Con 226+ articulos clave pre-identificados |
| **Referencias cruzadas UE** | 5 directivas/reglamentos europeos enlazados en 3 dominios |
| **Cache SQLite** | Evita llamadas repetidas a la API del BOE |
| **CLI completa** | 6 comandos para consulta directa desde terminal |

---

## Instalacion rapida

```bash
# Con uv (recomendado)
uvx normativa

# Con pip
pip install normativa
```

## Configuracion MCP rapida

Anade a tu `.mcp.json` (Claude Code, Cursor, VS Code):

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

## Primera consulta

```python
# Buscar por dominio tematico
buscar_por_dominio("fiscal", subtema="iva")

# Leer un articulo concreto
leer_articulo("BOE-A-2014-12328", "a29")
```

---

## Siguiente paso

Consulta la [guia de inicio rapido](guide/quickstart.md) para configuracion completa y ejemplos.

## Aviso legal

Este software tiene caracter informativo y **no constituye asesoramiento legal**. Consulte con un profesional antes de tomar decisiones basadas en los resultados obtenidos.

## Licencia

[MIT](https://github.com/ioseobcn/normativa/blob/main/LICENSE) -- InnovaOrigen 2026
