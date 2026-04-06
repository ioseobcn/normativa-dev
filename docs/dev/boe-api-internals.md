# API del BOE -- Internals

Todo lo que descubrimos sobre la API de datos abiertos del BOE durante el
desarrollo de normativa. Esta documentacion complementa la
[documentacion oficial](https://www.boe.es/datosabiertos/doc/API_BOE.pdf)
con el comportamiento real observado.

## Base URL

```
https://www.boe.es/datosabiertos/api
```

Todas las peticiones usan HTTPS. No hay autenticacion.

## Endpoints con comportamiento real

### GET /legislacion-consolidada

Lista de legislacion consolidada con filtros opcionales.

```
GET /legislacion-consolidada?limit=10&offset=0&from=20240101&to=20241231&query=impuesto
```

**Parametros**:

| Parametro | Tipo | Notas |
|-----------|------|-------|
| `limit` | int | Max real: **250** para listing. La documentacion dice 500, pero devuelve error con valores mayores a 250. |
| `offset` | int | Paginacion por offset, no por pagina. |
| `from` | string | Formato YYYYMMDD. Filtra por fecha de publicacion. |
| `to` | string | Formato YYYYMMDD. |
| `query` | string | **PROBLEMATICO**: devuelve 500 para muchas consultas de texto libre. Funciona mejor con terminos cortos y especificos. |

**Bugs conocidos**:

- El parametro `query` provoca HTTP 500 en muchos casos. No es fiable para
  busquedas de texto libre. Normativa lo usa pero tiene fallback al registro
  local cuando falla.
- Las `materias` NO son filtrables en este endpoint. El campo existe en
  `/analisis` por documento individual, pero no como filtro de listing.
- Valores de `limit` superiores a 250 causan error silencioso o respuesta
  truncada.

**Envelope de respuesta**:

```json
{
  "status": "OK",
  "total": 1234,
  "data": [
    {
      "identificador": "BOE-A-2006-20764",
      "titulo": "Ley 35/2006, de 28 de noviembre, del IRPF...",
      "rango": "Ley",
      "fecha_publicacion": "20061129",
      "estado_consolidacion": "Vigente",
      "url_eli": "https://www.boe.es/eli/es/l/2006/11/28/35/con"
    }
  ]
}
```

### GET /legislacion-consolidada/id/{BOE-ID}/metadatos

Metadatos completos de una norma.

```
GET /legislacion-consolidada/id/BOE-A-2006-20764/metadatos
Accept: application/json
```

**Respuesta**:

```json
{
  "status": "OK",
  "data": {
    "identificador": "BOE-A-2006-20764",
    "titulo": "Ley 35/2006, de 28 de noviembre, del IRPF...",
    "rango": "Ley",
    "numero_oficial": "35/2006",
    "fecha_publicacion": "20061129",
    "fecha_vigencia": "20070101",
    "estado_consolidacion": "Vigente",
    "departamento": "Jefatura del Estado",
    "url_eli": "https://www.boe.es/eli/es/l/2006/11/28/35/con",
    "materias": ["Impuestos", "IRPF"],
    "origen_legislativo": "Estatal",
    "notas": "Ultima actualizacion publicada 01/01/2024"
  }
}
```

**Notas**: El campo `data` a veces es un dict y a veces es una lista con
un solo elemento. Normativa maneja ambos casos en `obtener_metadatos()`.

### GET /legislacion-consolidada/id/{BOE-ID}/analisis

Referencias cruzadas y materias de una norma.

```
GET /legislacion-consolidada/id/BOE-A-2014-12328/analisis
```

**Respuesta**:

```json
{
  "status": "OK",
  "data": {
    "materias": ["Impuestos", "Impuesto sobre Sociedades"],
    "notas": "Texto consolidado vigente.",
    "afecta_a": [
      {"identificador": "BOE-A-2004-4456", "titulo": "RDLeg 4/2004", "tipo": "Deroga"}
    ],
    "afectada_por": [
      {"identificador": "BOE-A-2022-23042", "titulo": "Ley 28/2022", "tipo": "Modifica"}
    ]
  }
}
```

**Tipos de relacion observados**: `Deroga`, `Modifica`, `Complementa`,
`Desarrolla`, `Transpone`.

### GET /legislacion-consolidada/id/{BOE-ID}/texto/indice

Tabla de contenidos de una norma consolidada.

```
GET /legislacion-consolidada/id/BOE-A-2014-12328/texto/indice
Accept: application/json
```

**Respuesta** (con variantes de anidamiento):

```json
{
  "status": "OK",
  "data": {
    "items": [
      {
        "id": "tpreliminar",
        "titulo": "Titulo Preliminar. Naturaleza y ambito de aplicacion",
        "fecha_actualizacion": "20240101"
      },
      {
        "id": "a1",
        "titulo": "Articulo 1. Naturaleza",
        "fecha_actualizacion": "20240101"
      }
    ]
  }
}
```

**Variantes de anidamiento**: La API puede devolver `{"data": {"items": [...]}}`,
`{"data": [...]}`, `{"items": [...]}`, o directamente `[...]`. Normativa
maneja todas las variantes en `xml_parser.parse_indice()` y en
`BOEClient.legislacion_indice()`.

### GET /legislacion-consolidada/id/{BOE-ID}/texto/bloque/{bloque_id}

**Este endpoint es XML only**. Devuelve el texto de un articulo o seccion.

```
GET /legislacion-consolidada/id/BOE-A-2014-12328/texto/bloque/a29
Accept: application/xml
```

Si envias `Accept: application/json`, el servidor devuelve HTML en vez de
JSON o XML. Siempre pedir `application/xml`.

**Respuesta XML**:

```xml
<response status="OK">
  <data>
    <bloque id="a29" tipo="precepto" titulo="Articulo 29. Tipo de gravamen.">
      <version id_norma="BOE-A-2014-12328"
               fecha_publicacion="20141128"
               fecha_vigencia="20150101">
        <p class="articulo">Articulo 29. Tipo de gravamen.</p>
        <p class="parrafo">1. El tipo general de gravamen...</p>
        <p class="parrafo_2">No obstante, las entidades de nueva creacion...</p>
      </version>
    </bloque>
  </data>
</response>
```

### GET /boe/sumario/{YYYYMMDD}

Sumario diario del BOE.

```
GET /boe/sumario/20240315
```

El sumario tiene secciones anidadas (I, II, III, IV, V) con departamentos
dentro de cada seccion. Normativa aplana la estructura en
`_extraer_entradas_sumario()`.

### GET /borme/sumario/{YYYYMMDD}

Sumario diario del BORME. Misma estructura que el sumario BOE pero con
actos mercantiles.

### GET /datos-auxiliares/{tipo}

Tablas de referencia. Los tipos validos son:

- `materias` -- temas juridicos (codigos numericos + nombre)
- `departamentos` -- organismos emisores (ministerios, tribunales, etc.)
- `rangos` -- tipos de norma (Ley, Real Decreto, Orden, etc.)
- `ambitos` -- ambitos territoriales

## Formatos de ID

### BOE ID

```
BOE-A-YYYY-NNNNN    Legislacion
BOE-B-YYYY-NNNNN    Anuncios
BORME-S-YYYYMMDD    Sumarios BORME
```

Ejemplos reales:

- `BOE-A-2006-20764` -- Ley 35/2006 del IRPF
- `BOE-A-1992-28740` -- Ley 37/1992 del IVA
- `BOE-A-2014-12328` -- Ley 27/2014 del IS
- `BOE-A-2015-11430` -- Estatuto de los Trabajadores

### IDs de bloque

Los IDs de bloque **no son uniformes entre normas**. Siempre usar
`leer_indice` para obtener los IDs reales.

| Formato | Significado | Ejemplo |
|---------|-------------|---------|
| `a1`, `a29`, `a103` | Articulos numerados | Articulo 1, Articulo 29 |
| `a4bis` | Articulos con bis/ter | Articulo 4 bis (anadido por reforma) |
| `tpreliminar`, `t1`, `t2` | Titulos | Titulo Preliminar, Titulo I |
| `dadicional-primera`, `da1` | Disposiciones adicionales | DA 1a |
| `dtransitoria-primera`, `dt1` | Disposiciones transitorias | DT 1a |
| `dfinal-primera`, `df1` | Disposiciones finales | DF 1a |
| `dderogatoria-unica`, `dd1` | Disposiciones derogatorias | DD unica |
| `dfquinta`, `dtercera` | Formato abreviado (legacy) | DF 5a, DT 3a |
| `preambulo` | Preambulo | |
| `exposicion` | Exposicion de motivos | |
| `anexo-i`, `anexo-ii` | Anexos | |

**Trampa**: No todas las normas usan el mismo formato para disposiciones.
Algunas usan `dadicional-primera`, otras usan `da1`, y otras usan formatos
como `dfquinta`. El unico metodo fiable es consultar el indice primero.

## Formato de fechas

Todas las fechas en la API usan formato **YYYYMMDD** (sin separadores):

```
20240315  = 15 de marzo de 2024
20061129  = 29 de noviembre de 2006
```

La timezone es CET (Central European Time). No se documenta explicitamente
pero los sumarios se publican en hora peninsular espanola.

## Envelope de respuesta

La mayoria de endpoints devuelven este envelope:

```json
{
  "status": "OK",
  "data": { ... }
}
```

Pero hay variantes:

- A veces `status` es un objeto: `{"status": {"code": "200", "message": "OK"}}`
- A veces `data` es un array
- A veces no hay `status` y el dato esta directamente en la raiz
- Los endpoints de texto devuelven XML, no JSON

Normativa maneja todas las variantes con parsing defensivo en cada tool.

## Cuando la API devuelve HTML en vez de JSON

Esto ocurre en dos situaciones:

1. **Pedir JSON a un endpoint de texto**: Si envias `Accept: application/json`
   a `/texto/bloque/`, el servidor devuelve HTML (la pagina web del BOE).
   Solucion: siempre usar `Accept: application/xml` para endpoints de texto.

2. **Server overload**: Cuando el servidor esta sobrecargado, a veces devuelve
   una pagina HTML de error en vez del JSON esperado. `httpx` lanzara una
   excepcion al intentar parsear como JSON. El retry del client maneja esto.

## Rate limiting observado

No hay headers de rate limit documentados (`X-RateLimit-*`). Pero hemos
observado:

- Con mas de ~5 req/s el servidor empieza a devolver 503
- Con picos de trafico, los tiempos de respuesta suben de 200ms a 2-3 segundos
- No hay ban permanente observado, solo degradacion temporal

Normativa limita a 2 req/s por precaucion.

## Errores frecuentes

| Situacion | Codigo HTTP | Causa |
|-----------|-------------|-------|
| Query compleja en listing | 500 | Bug del servidor con ciertos terminos de busqueda |
| BOE ID inexistente | 404 | |
| Bloque ID inexistente | 404 | Verificar con indice primero |
| Tipo de datos auxiliares invalido | 400 | Solo: materias, departamentos, rangos, ambitos |
| Fecha futura en sumario | 404 | No hay sumario para el futuro |
| JSON a endpoint de texto | 200 (HTML) | No es error HTTP, pero el body no es JSON ni XML |

## Tips para desarrollo

1. **Verificar BOE IDs con curl**:
   ```bash
   curl -s -H "Accept: application/json" \
     "https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/BOE-A-2006-20764/metadatos" \
     | python3 -m json.tool
   ```

2. **Verificar indice**:
   ```bash
   curl -s -H "Accept: application/json" \
     "https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/BOE-A-2006-20764/texto/indice" \
     | python3 -m json.tool
   ```

3. **Leer un bloque XML**:
   ```bash
   curl -s -H "Accept: application/xml" \
     "https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/BOE-A-2006-20764/texto/bloque/a1"
   ```

4. **Sumario de hoy**:
   ```bash
   curl -s -H "Accept: application/json" \
     "https://www.boe.es/datosabiertos/api/boe/sumario/$(date +%Y%m%d)" \
     | python3 -m json.tool
   ```
