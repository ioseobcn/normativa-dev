# API del BOE

`normativa` consume la [API de datos abiertos del BOE](https://www.boe.es/datosabiertos/) (Agencia Estatal Boletin Oficial del Estado).

## Base URL

```
https://www.boe.es/datosabiertos/api
```

## Endpoints utilizados

### Legislacion consolidada

| Endpoint | Metodo | Descripcion |
|---|---|---|
| `/legislacion-consolidada` | GET | Lista legislacion con filtros |
| `/legislacion-consolidada/id/{boe_id}/metadatos` | GET | Metadatos de una disposicion |
| `/legislacion-consolidada/id/{boe_id}/analisis` | GET | Analisis juridico (materias, referencias) |
| `/legislacion-consolidada/id/{boe_id}/texto/indice` | GET | Indice de articulos |
| `/legislacion-consolidada/id/{boe_id}/texto/bloque/{bloque_id}` | GET | Texto de un articulo (XML) |

### Sumarios

| Endpoint | Metodo | Descripcion |
|---|---|---|
| `/boe/sumario/{fecha}` | GET | Sumario diario del BOE |
| `/borme/sumario/{fecha}` | GET | Sumario diario del BORME |

### Datos auxiliares

| Endpoint | Metodo | Descripcion |
|---|---|---|
| `/datos-auxiliares/materias` | GET | Lista de materias juridicas |
| `/datos-auxiliares/departamentos` | GET | Organismos emisores |
| `/datos-auxiliares/rangos` | GET | Tipos de norma |
| `/datos-auxiliares/ambitos` | GET | Ambitos territoriales |

## Formato de fechas

La API acepta fechas en formato `YYYYMMDD` (ej: `20260405`).

`normativa` acepta internamente `YYYY-MM-DD`, `DD/MM/YYYY` y `YYYYMMDD`, convirtiendo automaticamente.

## Formato de respuesta

- **Metadatos, analisis, sumarios, legislacion**: JSON
- **Texto de articulos (bloques)**: XML

`normativa` parsea el XML automaticamente y lo convierte a Markdown limpio.

## Parametros de lista

| Parametro | Tipo | Descripcion |
|---|---|---|
| `limit` | int | Maximo resultados por pagina |
| `offset` | int | Desplazamiento para paginacion |
| `from` | str | Fecha inicio (YYYYMMDD) |
| `to` | str | Fecha fin (YYYYMMDD) |
| `query` | str | Texto de busqueda |

## Limitaciones conocidas

### Busqueda por query limitada a ~500 resultados

La busqueda por texto libre (`query`) en `/legislacion-consolidada` devuelve un maximo de ~500 resultados independientemente del `limit` solicitado. Para busquedas mas amplias, `normativa` usa el registro local de dominios como complemento.

### Materias no filtrables directamente

El endpoint de lista no permite filtrar por materia. `normativa` resuelve esto pre-mapeando las materias BOE en cada dominio y construyendo queries con terminos optimizados.

### Texto solo en XML

Los bloques de texto (articulos) se devuelven en XML. No hay endpoint JSON para textos. `normativa` parsea el XML con `defusedxml` y lo convierte a Markdown.

### Rate limiting

La API no documenta limites de rate, pero `normativa` implementa:

- Maximo 2 requests/segundo
- Retry con backoff exponencial (3 intentos)
- Timeout de 30 segundos por request

### Disponibilidad

La API puede tener caidas puntuales. `normativa` tiene un fallback al registro local de dominios que devuelve las leyes clave pre-mapeadas sin necesidad de conexion.

## Identificadores BOE

El formato de un BOE ID es: `BOE-{tipo}-{anno}-{numero}`

- `BOE-A-2006-20764` -- Disposicion (A = seccion del BOE)
- `BOE-A-2014-12328` -- Otra disposicion

El `bloque_id` para articulos sigue el patron `a{numero}` (ej: `a29` para articulo 29). Otros bloques pueden ser `dt1` (disposicion transitoria 1), `da1` (disposicion adicional 1), etc.
