# Skill: API BOE — Referencia tecnica para agentes

## Cuando cargar
ACTIVAR cuando: un agente necesita resolver dudas sobre como usar las herramientas MCP de normativa
NO ACTIVAR cuando: el agente ya sabe que herramienta usar y como

## Herramientas MCP disponibles

Prefijo en Claude Code: `mcp__normativa__`

### Busqueda

#### buscar_legislacion
- **Uso**: Busqueda libre por texto en legislacion consolidada
- **Cuando**: Busqueda exploratoria, terminos no asociados a un dominio claro
- **Limitacion**: La busqueda por texto puede ser inconsistente. Probar variaciones terminologicas si no hay resultados (ej: "despido" vs "extincion del contrato de trabajo")
- **Tip**: Usar terminos juridicos precisos, no coloquiales

#### buscar_por_dominio
- **Uso**: Busqueda filtrada por dominio tematico
- **Cuando**: Se conoce el dominio (fiscal, laboral, mercantil, autonomos, proteccion_datos, digital, vivienda)
- **Parametros**: dominio (obligatorio), subtema (recomendado para acotar)
- **Preferir sobre**: buscar_legislacion cuando el dominio es claro

#### listar_dominios
- **Uso**: Lista los dominios tematicos disponibles en el sistema
- **Cuando**: Para confirmar que dominios existen antes de buscar_por_dominio
- **Devuelve**: Array de slugs de dominio

### Metadatos y analisis

#### obtener_metadatos
- **Uso**: Metadatos de una norma (vigencia, fechas, departamento, origen)
- **Cuando**: Verificar si una norma esta vigente, cuando fue publicada, cuando fue modificada por ultima vez
- **Parametro**: BOE ID (ej: BOE-A-2015-11430)
- **Devuelve**: estado de vigencia, fecha de publicacion, fecha de ultima modificacion, departamento emisor, materias
- **Limitacion**: El campo "materias" no siempre esta bien categorizado en la fuente

#### obtener_analisis
- **Uso**: Analisis de referencias cruzadas de una norma
- **Cuando**: Para ver que normas referencia y que normas la referencian
- **Devuelve**: Lista de normas citadas, normas que la citan, modificaciones recibidas
- **Tip**: Util para descubrir normativa relacionada que no aparecio en la busqueda

### Lectura de texto

#### leer_indice
- **Uso**: Obtiene el indice estructurado de una norma (titulos, capitulos, secciones, articulos, disposiciones)
- **Cuando**: SIEMPRE antes de leer articulos concretos, para confirmar que existen y obtener sus IDs de bloque
- **Devuelve**: Estructura jerarquica con ID de bloque para cada elemento
- **CRITICO**: Paso obligatorio antes de leer_articulo

#### leer_articulo
- **Uso**: Texto de un bloque concreto (articulo, disposicion adicional, transitoria, etc.)
- **Parametros**: BOE ID + ID de bloque
- **Devuelve**: Texto completo del bloque en formato texto

#### leer_articulos_rango
- **Uso**: Lee varios articulos consecutivos de una vez
- **Cuando**: Para extraer bloques contiguos (ej: arts. 15 a 20)
- **Mas eficiente que**: Llamar leer_articulo 6 veces
- **Limitacion**: Solo para articulos consecutivos dentro de la misma norma

### Sumarios

#### sumario_boe
- **Uso**: Sumario del BOE para una fecha concreta
- **Parametro**: Fecha (YYYY-MM-DD)
- **Devuelve**: Lista de publicaciones del dia con: seccion, departamento, titulo, ID
- **Cuando**: Para monitorizar publicaciones recientes
- **Limitacion**: Solo un dia por llamada. Para periodos, iterar por dias

#### sumario_borme
- **Uso**: Sumario del BORME para una fecha concreta
- **Parametro**: Fecha (YYYY-MM-DD)
- **Devuelve**: Publicaciones del BORME (actos mercantiles, resoluciones)
- **Cuando**: Para temas mercantiles/registrales

### Auxiliares

#### datos_auxiliares
- **Uso**: Tablas auxiliares del sistema (departamentos, materias, origenes)
- **Cuando**: Para entender los codigos usados en metadatos
- **Devuelve**: Listas de referencia

## Formatos de ID

### BOE ID
- Formato: `BOE-A-YYYY-XXXXX` (legislacion)
- Formato: `BOE-B-YYYY-XXXXX` (anuncios)
- Ejemplo: `BOE-A-2015-11430` (Estatuto de los Trabajadores)

### IDs de bloque (para leer_articulo)
- Articulos: `a1`, `a2`, `a15`, `a103`
- Disposiciones adicionales: `dadicional-primera`, `dadicional-segunda` o `da1`, `da2`
- Disposiciones transitorias: `dtransitoria-primera` o `dt1`, `dt2`
- Disposiciones finales: `dfinal-primera` o `df1`, `df2`
- Disposiciones derogatorias: `dderogatoria-unica` o `dd1`
- Preambulo: `preambulo`
- Exposicion de motivos: `exposicion`
- Anexos: `anexo-i`, `anexo-ii`

**IMPORTANTE**: Los IDs de bloque varian entre normas. SIEMPRE usar `leer_indice` primero para obtener los IDs reales de cada norma. No asumir el formato.

## Limitaciones conocidas

1. **Materias no filtrables**: El campo "materias" en metadatos no es fiable para filtrar. Usar buscar_por_dominio en su lugar.
2. **Texto solo XML en la fuente**: El texto original del BOE es XML. La API devuelve texto limpio pero puede perder formato de tablas complejas.
3. **Busqueda por texto inconsistente**: buscar_legislacion puede no encontrar resultados con terminos vagos. Usar terminos juridicos precisos y probar sinonimos.
4. **Sumarios limitados a un dia**: sumario_boe y sumario_borme solo devuelven un dia por llamada.
5. **Normas preconstitucionales**: Algunas normas muy antiguas pueden tener indices incompletos o IDs de bloque irregulares.
6. **Texto consolidado vs original**: El texto devuelto es el consolidado (con modificaciones incorporadas). Para ver la version original de un articulo antes de una modificacion, no hay herramienta directa.

## Patrones de uso recomendados

### Buscar normativa por tema
```
listar_dominios -> buscar_por_dominio(dominio, subtema) -> obtener_metadatos(BOE_ID) -> obtener_analisis(BOE_ID)
```

### Extraer articulos concretos
```
leer_indice(BOE_ID) -> confirmar IDs de bloque -> leer_articulo(BOE_ID, bloque_id)
```

### Monitorizar cambios
```
sumario_boe(fecha) -> filtrar por departamento -> obtener_metadatos(BOE_ID)
```

### Busqueda amplia (cuando buscar_por_dominio no basta)
```
buscar_legislacion(termino1) + buscar_legislacion(termino2) -> deduplicar -> obtener_metadatos
```
