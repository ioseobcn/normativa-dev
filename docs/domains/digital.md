# Digital

**Derecho Digital y Comercio Electronico**

Legislacion espanola sobre sociedad de la informacion, comercio electronico, servicios digitales, firma electronica y regulacion de plataformas en linea.

## Leyes clave

### LSSI (BOE-A-2002-13758)

Ley 34/2002, de 11 de julio, de servicios de la sociedad de la informacion y de comercio electronico.

| Articulo | Contenido |
|---|---|
| `a5` | Deber de informacion general (aviso legal) |
| `a10` | Constancia registral del nombre de dominio |
| `a12` | Deber de retencion de datos de trafico |
| `a20` | Informacion sobre comunicaciones comerciales |
| `a21` | Prohibicion de spam |
| `a22` | Derechos de los destinatarios |
| `a23` | Validez de los contratos electronicos |
| `a27` | Obligaciones previas a la contratacion |
| `a28` | Informacion posterior al contrato |
| `a38` | Infracciones |
| `a39` | Sanciones |

**Referencia UE:**

- Transpone la [Directiva 2000/31/CE](http://data.europa.eu/eli/dir/2000/31/oj) sobre comercio electronico
- Transpone la [Directiva 2002/58/CE](http://data.europa.eu/eli/dir/2002/58/oj) sobre privacidad en comunicaciones electronicas (ePrivacy)

### Ley Servicios Confianza (BOE-A-2020-14046)

Ley 6/2020, reguladora de determinados aspectos de los servicios electronicos de confianza.

| Articulo | Contenido |
|---|---|
| `a1` | Objeto de la ley |
| `a3` | Firma electronica y documentos electronicos |
| `a4` | Efectos juridicos de la firma electronica |
| `a6` | Identidad y atributos de los certificados |
| `a9` | Certificados cualificados |
| `a12` | Sellos electronicos de tiempo |
| `a14` | Obligaciones de prestadores de servicios de confianza |

## Subtemas

- **comercio_electronico** -- Aviso legal, condiciones de contratacion online, informacion al consumidor
- **comunicaciones_comerciales** -- Email marketing, cookies, consentimiento del usuario
- **firma_electronica** -- Tipos de firma (simple, avanzada, cualificada), certificados digitales, sellos de tiempo

## Casos de uso

```python
# Requisitos legales para una tienda online
buscar_por_dominio("digital", subtema="comercio_electronico")

# Verificar obligaciones de aviso legal
leer_articulo("BOE-A-2002-13758", "a5")

# Consultar validez de firma electronica
leer_articulo("BOE-A-2020-14046", "a4")
```
