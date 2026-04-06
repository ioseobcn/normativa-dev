# Tools MCP

Referencia completa de las 11 herramientas MCP que expone `normativa`.

Todas las herramientas son funciones async que devuelven `dict`. FastMCP serializa automaticamente a JSON.

---

## Busqueda

### `buscar_legislacion`

Busqueda de texto libre en legislacion consolidada del BOE.

**Parametros:**

| Parametro | Tipo | Default | Descripcion |
|---|---|---|---|
| `query` | `str` | (requerido) | Texto libre de busqueda |
| `rango` | `str` | `""` | Filtro por tipo de norma (Ley, Real Decreto, Orden...) |
| `departamento` | `str` | `""` | Organismo emisor |
| `ambito` | `str` | `""` | Ambito territorial |
| `fecha_desde` | `str` | `""` | Fecha inicio (YYYYMMDD) |
| `fecha_hasta` | `str` | `""` | Fecha fin (YYYYMMDD) |
| `limit` | `int` | `10` | Maximo resultados (max 50) |
| `offset` | `int` | `0` | Paginacion |

**Retorna:**

```json
{
  "total": 42,
  "offset": 0,
  "limit": 10,
  "resultados": [
    {
      "boe_id": "BOE-A-2006-20764",
      "titulo": "Ley 35/2006, del IRPF...",
      "rango": "Ley",
      "fecha": "2006-11-29",
      "estado": "Vigente",
      "url": "..."
    }
  ]
}
```

Si la API del BOE no esta disponible, devuelve resultados del registro local de dominios con `"fuente": "registro_local"`.

### `buscar_por_dominio`

Busqueda por dominio tematico. **La herramienta diferenciadora de normativa.**

**Parametros:**

| Parametro | Tipo | Default | Descripcion |
|---|---|---|---|
| `dominio` | `str` | `""` | Clave del dominio (fiscal, laboral, mercantil...) |
| `subtema` | `str` | `""` | Subtema dentro del dominio (irpf, despido...) |
| `caso_uso` | `str` | `""` | Descripcion libre del caso para refinar busqueda |

**Retorna:**

```json
{
  "dominio": "fiscal",
  "nombre_dominio": "Derecho Fiscal y Tributario",
  "subtema": "iva",
  "query_generada": "IVA valor anadido tipo impositivo...",
  "total": 15,
  "resultados": [...],
  "leyes_clave": [
    {
      "boe_id": "BOE-A-1992-28740",
      "nombre_corto": "Ley IVA",
      "rango": "Ley",
      "eu_refs": [{"celex": "32006L0112", "titulo": "Directiva IVA", ...}]
    }
  ]
}
```

---

## Metadatos y analisis

### `obtener_metadatos`

Metadatos completos de una disposicion del BOE.

**Parametros:**

| Parametro | Tipo | Descripcion |
|---|---|---|
| `boe_id` | `str` | Identificador BOE (ej: `BOE-A-2006-20764`) |

**Retorna:** `{"boe_id": "...", "data": {...}}` con titulo, rango, fecha, departamento, estado, materias, url ELI.

### `obtener_analisis`

Analisis juridico: materias y referencias cruzadas (afecta a / afectada por).

**Parametros:**

| Parametro | Tipo | Default | Descripcion |
|---|---|---|---|
| `boe_id` | `str` | (requerido) | Identificador BOE |
| `incluir_referencias` | `bool` | `True` | Incluir normas que afecta/es afectada por |
| `max_referencias` | `int` | `20` | Limite de referencias por tipo |

**Retorna:** `{"boe_id": "...", "materias": [...], "afecta_a": [...], "afectada_por": [...]}`.

---

## Lectura de textos

### `leer_indice`

Tabla de contenidos de una norma consolidada.

**Parametros:**

| Parametro | Tipo | Descripcion |
|---|---|---|
| `boe_id` | `str` | Identificador BOE |

**Retorna:**

```json
{
  "boe_id": "BOE-A-2014-12328",
  "total_bloques": 148,
  "indice": [
    {"id": "a1", "titulo": "Naturaleza del impuesto"},
    {"id": "a2", "titulo": "Ambito de aplicacion espacial"},
    ...
  ]
}
```

### `leer_articulo`

Lee UN articulo/bloque concreto como Markdown. **La herramienta principal de lectura.**

**Parametros:**

| Parametro | Tipo | Descripcion |
|---|---|---|
| `boe_id` | `str` | Identificador BOE |
| `bloque_id` | `str` | ID del bloque (ej: `a29`) -- obtenlo de `leer_indice()` |

**Retorna:**

```json
{
  "boe_id": "BOE-A-2014-12328",
  "bloque_id": "a29",
  "titulo": "Articulo 29. Tipo de gravamen.",
  "tipo": "articulo",
  "version": {"fecha": "...", "estado": "vigente"},
  "texto": "## Articulo 29. Tipo de gravamen.\n\n1. El tipo general..."
}
```

### `leer_articulos_rango`

Lee un rango consecutivo de articulos. Limitado para no saturar el contexto.

**Parametros:**

| Parametro | Tipo | Default | Descripcion |
|---|---|---|---|
| `boe_id` | `str` | (requerido) | Identificador BOE |
| `desde` | `str` | (requerido) | ID del primer bloque |
| `hasta` | `str` | (requerido) | ID del ultimo bloque |
| `max_bloques` | `int` | `10` | Maximo de bloques (hard cap: 20) |

**Retorna:** `{"boe_id": "...", "articulos": [{bloque_id, titulo, texto}, ...], "truncado": false}`.

---

## Sumarios diarios

### `sumario_boe`

Sumario diario del BOE, filtrable por seccion, departamento o dominio.

**Parametros:**

| Parametro | Tipo | Default | Descripcion |
|---|---|---|---|
| `fecha` | `str` | hoy | Fecha (YYYY-MM-DD, DD/MM/YYYY o YYYYMMDD) |
| `seccion` | `str` | `""` | Seccion del BOE (I, II, III, IV, V) |
| `departamento` | `str` | `""` | Departamento emisor |
| `dominio` | `str` | `""` | Dominio tematico para filtrar |

**Retorna:** `{"fecha": "...", "total": 42, "entradas": [{boe_id, titulo, seccion, departamento, rango, url_pdf}, ...]}`.

### `sumario_borme`

Sumario diario del BORME (Boletin Oficial del Registro Mercantil).

**Parametros:**

| Parametro | Tipo | Default | Descripcion |
|---|---|---|---|
| `fecha` | `str` | hoy | Fecha del sumario |

**Retorna:** mismo formato que `sumario_boe`.

---

## Dominios y auxiliares

### `listar_dominios`

Lista todos los dominios tematicos disponibles con metadatos.

**Sin parametros.**

**Retorna:**

```json
{
  "total": 14,
  "dominios": [
    {
      "clave": "fiscal",
      "nombre": "Derecho Fiscal y Tributario",
      "descripcion": "...",
      "subtemas": ["irpf", "iva", "impuesto_sociedades", "tributaria_general"],
      "leyes_clave": [{"boe_id": "BOE-A-2006-20764", "nombre": "Ley IRPF"}, ...],
      "enriquecido": true
    }
  ]
}
```

### `datos_auxiliares`

Datos de referencia del BOE: materias, departamentos, rangos y ambitos.

**Parametros:**

| Parametro | Tipo | Default | Descripcion |
|---|---|---|---|
| `tipo` | `str` | (requerido) | `materias`, `departamentos`, `rangos` o `ambitos` |
| `buscar` | `str` | `""` | Texto para filtrar resultados |

**Retorna:** `{"tipo": "materias", "total": 200, "items": [...]}`.
