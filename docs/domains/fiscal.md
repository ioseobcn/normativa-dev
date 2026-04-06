# Fiscal

**Derecho Fiscal y Tributario**

Legislacion tributaria espanola: impuestos sobre la renta (IRPF), valor anadido (IVA), sociedades (IS) y normas generales tributarias. Cubre obligaciones fiscales de personas fisicas, juridicas y no residentes.

## Leyes clave

### Ley IRPF (BOE-A-2006-20764)

Ley 35/2006, de 28 de noviembre, del Impuesto sobre la Renta de las Personas Fisicas.

| Articulo | Contenido |
|---|---|
| `a6` | Hecho imponible |
| `a7` | Rentas exentas |
| `a17` | Rendimientos integros del trabajo |
| `a19` | Gastos deducibles de rendimientos del trabajo |
| `a27` | Rendimientos integros de actividades economicas |
| `a33` | Concepto de ganancia o perdida patrimonial |
| `a46` | Base liquidable general y del ahorro |
| `a68` | Deduccion por inversion en vivienda habitual (regimen transitorio) |
| `a80` | Deduccion por maternidad |
| `a96` | Obligacion de declarar |
| `a101` | Retenciones e ingresos a cuenta |

### Ley IVA (BOE-A-1992-28740)

Ley 37/1992, de 28 de diciembre, del Impuesto sobre el Valor Anadido.

| Articulo | Contenido |
|---|---|
| `a4` | Hecho imponible |
| `a5` | Concepto de empresario o profesional |
| `a20` | Exenciones en operaciones interiores |
| `a78` | Base imponible: regla general |
| `a90` | Tipo impositivo general |
| `a91` | Tipos impositivos reducidos |
| `a94` | Operaciones que generan derecho a deducir |
| `a99` | Regla de prorrata |
| `a164` | Obligaciones formales: facturas, libros, declaraciones |

**Referencia UE:** Transpone la [Directiva 2006/112/CE](http://data.europa.eu/eli/dir/2006/112/oj) relativa al sistema comun del IVA.

### Ley IS (BOE-A-2014-12328)

Ley 27/2014, de 27 de noviembre, del Impuesto sobre Sociedades.

| Articulo | Contenido |
|---|---|
| `a4` | Hecho imponible |
| `a7` | Sujeto pasivo |
| `a10` | Concepto y determinacion de la base imponible |
| `a12` | Correcciones de valor: amortizaciones |
| `a15` | Gastos no deducibles |
| `a16` | Limitacion a la deducibilidad de gastos financieros |
| `a26` | Compensacion de bases imponibles negativas |
| `a29` | Tipo de gravamen |
| `a36` | Deduccion para evitar doble imposicion internacional |

**Referencia UE:** Implementa la [Directiva (UE) 2016/1164](http://data.europa.eu/eli/dir/2016/1164/oj) contra las practicas de elusion fiscal (ATAD).

### LGT (BOE-A-2003-23186)

Ley 58/2003, de 17 de diciembre, General Tributaria.

| Articulo | Contenido |
|---|---|
| `a2` | Concepto, fines y clases de tributos |
| `a15` | Conflicto en la aplicacion de la norma tributaria |
| `a26` | Intereses de demora |
| `a27` | Recargos por declaracion extemporanea |
| `a34` | Derecho de los obligados tributarios |
| `a66` | Plazos de prescripcion |
| `a178` | Principio de no concurrencia de sanciones |
| `a191` | Infraccion tributaria por dejar de ingresar |

## Subtemas

- **irpf** -- IRPF: rendimientos del trabajo, capital, actividades economicas, ganancias patrimoniales, deducciones
- **iva** -- IVA: tipos impositivos, exenciones, deducciones, regimenes especiales, obligaciones formales
- **impuesto_sociedades** -- IS: base imponible, gastos deducibles, tipo de gravamen, deducciones, consolidacion fiscal
- **tributaria_general** -- LGT: procedimientos de gestion, inspeccion, recaudacion, sanciones, prescripcion

## Casos de uso

```bash
# Consultar tipo de IVA aplicable
normativa buscar "tipo IVA" --dominio fiscal

# Leer el articulo sobre el tipo de gravamen del IS
normativa articulo BOE-A-2014-12328 a29

# Ver tramos IRPF
normativa dominio fiscal --subtema irpf
```

## Ejemplo MCP

```python
# Buscar legislacion fiscal sobre IVA
buscar_por_dominio("fiscal", subtema="iva")

# Leer articulo sobre rentas exentas
leer_articulo("BOE-A-2006-20764", "a7")

# Obtener analisis de la LGT
obtener_analisis("BOE-A-2003-23186")
```
