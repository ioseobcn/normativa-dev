# Laboral

**Derecho Laboral y Seguridad Social**

Legislacion laboral espanola: relaciones individuales y colectivas de trabajo, Seguridad Social, prevencion de riesgos laborales. Cubre contratos, despidos, salarios, prestaciones y cotizaciones.

## Leyes clave

### Estatuto de los Trabajadores (BOE-A-2015-11430)

RDLeg 2/2015, de 23 de octubre, texto refundido de la Ley del Estatuto de los Trabajadores.

| Articulo | Contenido |
|---|---|
| `a1` | Ambito de aplicacion |
| `a4` | Derechos laborales |
| `a8` | Forma del contrato |
| `a12` | Contrato a tiempo parcial y de relevo |
| `a14` | Periodo de prueba |
| `a15` | Duracion del contrato de trabajo |
| `a26` | Del salario |
| `a27` | Salario minimo interprofesional |
| `a34` | Jornada |
| `a37` | Descanso semanal, fiestas y permisos |
| `a38` | Vacaciones anuales |
| `a41` | Modificaciones sustanciales de condiciones de trabajo |
| `a49` | Extincion del contrato |
| `a51` | Despido colectivo |
| `a52` | Extincion por causas objetivas |
| `a54` | Despido disciplinario |
| `a56` | Despido improcedente |

### LGSS (BOE-A-2015-11724)

RDLeg 8/2015, Ley General de la Seguridad Social.

| Articulo | Contenido |
|---|---|
| `a2` | Fines de la Seguridad Social |
| `a7` | Extension del campo de aplicacion |
| `a16` | Afiliacion, altas y bajas |
| `a19` | Bases y tipos de cotizacion |
| `a169` | Situacion legal de desempleo |
| `a204` | Condiciones generales de acceso a la jubilacion |
| `a205` | Edad de jubilacion |
| `a248` | Incapacidad temporal |

### Ley PRL (BOE-A-1995-24292)

Ley 31/1995, de Prevencion de Riesgos Laborales.

| Articulo | Contenido |
|---|---|
| `a14` | Derecho a la proteccion frente a riesgos laborales |
| `a15` | Principios de la accion preventiva |
| `a16` | Plan de prevencion y evaluacion de riesgos |
| `a19` | Formacion de los trabajadores |
| `a22` | Vigilancia de la salud |

## Subtemas

- **contratos** -- Tipos de contratos laborales, formalizacion, periodo de prueba, duracion, modalidades
- **despido** -- Despido disciplinario, objetivo, colectivo (ERE), indemnizaciones
- **seguridad_social** -- Afiliacion, cotizacion, prestaciones (desempleo, jubilacion, IT)
- **prevencion_riesgos** -- Obligaciones empresariales en PRL, evaluacion de riesgos

## Casos de uso

```python
# Consultar requisitos de despido
buscar_por_dominio("laboral", subtema="despido")

# Leer articulo sobre despido improcedente
leer_articulo("BOE-A-2015-11430", "a56")

# Verificar edad de jubilacion
leer_articulo("BOE-A-2015-11724", "a205")
```
