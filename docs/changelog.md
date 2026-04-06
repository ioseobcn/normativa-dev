# Changelog

## v0.1.0 (2026-04-05)

Release inicial.

### MCP Server

- 11 herramientas MCP via FastMCP: buscar_legislacion, buscar_por_dominio, obtener_metadatos, obtener_analisis, leer_indice, leer_articulo, leer_articulos_rango, sumario_boe, sumario_borme, listar_dominios, datos_auxiliares

### Dominios tematicos

- 7 dominios enriquecidos con `DomainConfig`: fiscal, laboral, mercantil, autonomos, proteccion_datos, digital, vivienda
- 17 leyes espanolas mapeadas con 226+ articulos clave identificados
- 5 referencias cruzadas a legislacion UE en 3 dominios (fiscal, proteccion_datos, digital)
- 7 dominios basicos adicionales con busqueda por keywords

### Agentes

- 6 agentes legales: investigador-legal, monitor-cambios, extractor-articulos, analista-dominio, verificador-cumplimiento, redactor-informes
- 3 agentes de desarrollo: dev-contributor, dev-domain-builder, dev-tester
- Pipeline de investigacion en 4 fases con comunicacion via handoff/

### CLI

- 6 comandos: buscar, dominio, articulo, indice, sumario, serve
- Salida tabla o JSON
- Formatos de fecha flexibles

### Infraestructura

- Cache SQLite para evitar llamadas repetidas a la API del BOE
- Fallback a registro local cuando la API no esta disponible
- Rate limiting (2 req/s) y retry con backoff exponencial
- Parser XML a Markdown para textos legales
