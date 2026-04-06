# Autonomos

**Trabajo Autonomo y Emprendedores**

Legislacion del trabajo autonomo en Espana: Estatuto del Trabajo Autonomo (LETA), cotizacion al RETA, fiscalidad del autonomo (IRPF/IVA), facturacion y obligaciones formales. Dominio transversal con fiscal y laboral.

## Leyes clave

### LETA (BOE-A-2007-13409)

Ley 20/2007, de 11 de julio, del Estatuto del trabajo autonomo.

| Articulo | Contenido |
|---|---|
| `a1` | Concepto y ambito subjetivo |
| `a3` | Derechos profesionales del trabajador autonomo |
| `a4` | Deberes profesionales basicos |
| `a5` | Derechos del TRADE |
| `a11` | Contratacion del TRADE |
| `a12` | Jornada y descansos del TRADE |
| `a14` | Extincion del contrato del TRADE |
| `a16` | Prevision social y proteccion por cese de actividad |

### Ley IRPF -- ref. autonomos (BOE-A-2006-20764)

Articulos especificos de la Ley IRPF que afectan al autonomo.

| Articulo | Contenido |
|---|---|
| `a27` | Rendimientos integros de actividades economicas |
| `a28` | Reglas generales calculo rendimiento neto |
| `a30` | Estimacion directa |
| `a31` | Estimacion objetiva (modulos) |
| `a101` | Retenciones e ingresos a cuenta |

### LGSS -- RETA (BOE-A-2015-11724)

Articulos del RETA en la Ley General de la Seguridad Social.

| Articulo | Contenido |
|---|---|
| `a305` | Campo de aplicacion del RETA |
| `a306` | Afiliacion y alta en el RETA |
| `a307` | Cotizacion en el RETA |
| `a308` | Accion protectora en el RETA |
| `a327` | Prestacion por cese de actividad |
| `a329` | Requisitos para la prestacion por cese |
| `a331` | Duracion y cuantia del cese de actividad |

## Subtemas

- **alta_autonomo** -- Tramites de alta en Hacienda (modelo 036/037) y RETA
- **cotizacion_reta** -- Bases de cotizacion por ingresos reales, cuotas, tarifa plana
- **fiscalidad_autonomo** -- IRPF en actividades economicas, IVA, pagos fraccionados, gastos deducibles
- **facturacion** -- Requisitos de facturacion, factura electronica, Verifactu, obligaciones formales

## Casos de uso

```python
# Consultar tramites de alta como autonomo
buscar_por_dominio("autonomos", subtema="alta_autonomo")

# Verificar cotizacion al RETA
leer_articulo("BOE-A-2015-11724", "a307")

# Consultar gastos deducibles
buscar_por_dominio("autonomos", caso_uso="gastos deducibles autonomo")
```
