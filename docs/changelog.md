# Changelog

## v0.2.0 (2026-08-19)

Los 13 tools verificados en vivo contra la API real del BOE.

### Corregido

- **Busqueda reparada**: el param `query` de la API BOE exige JSON estilo
  Elasticsearch (`query_string` sobre `titulo:`); el texto plano devolvia
  500 siempre. Nuevo `build_query_param()` con saneo de caracteres Lucene
  y operador AND/OR. `buscar_legislacion` y `buscar_por_dominio` consultan
  por fin la API real en vez de caer al registro local.
- **`leer_articulo` devolvia redacciones derogadas**: cada bloque trae una
  `<version>` por consolidacion y se leia la primera (la mas antigua).
  Ahora se selecciona la version vigente hoy.
- `leer_indice` devolvia 0 bloques (envelope real `data[0].bloque[]`);
  arrastraba tambien a `leer_articulos_rango`.
- `obtener_analisis` devolvia vacio: reescrito con las claves reales
  (`materias[].materia`, `referencias.anteriores/posteriores`) —
  ahora expone afecta_a/afectada_por con relacion (DEROGA, MODIFICA...).
- `sumario_boe`/`sumario_borme` devolvian 0 entradas: el extractor recorre
  la jerarquia real `diario[].seccion[].departamento[].[epigrafe[]].item[]`
  conservando el contexto de cada entrada.
- Fixtures de tests regenerados con los envelopes reales de la API (los
  anteriores validaban un formato inventado y daban verde falso).

### Anadido

- **`leer_norma_ue`**: acceso al derecho de la UE publicado en el DOUE
  (AI Act, RGPD, DSA...) via el XML que sirve el BOE. Patron
  indice→articulo, tablas en Markdown, acepta CELEX mapeado. El AI Act
  (DOUE-L-2024-81079) queda mapeado en el dominio digital.
- **`historial_versiones`**: redacciones historicas de un articulo con la
  norma modificadora y fechas; recupera el texto de una version concreta.
- `leer_articulo` acepta numero de articulo ("48", "articulo 48",
  "13 bis") y sugiere ids similares ante un bloque inexistente.
- `DomainConfig.normas_ue` + `EURef.doue_id` para derecho UE directamente
  aplicable, visible en `buscar_por_dominio` y `listar_dominios`.
- Cache de sumarios (TTL 6h hoy / 30 dias pasados) y de documentos DOUE.
- `BOEAPIError`: mensajes de error cortos y en espanol.

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
