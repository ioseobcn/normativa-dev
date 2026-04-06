# Vivienda

**Derecho de la Vivienda y Arrendamientos**

Legislacion espanola sobre vivienda: Ley por el Derecho a la Vivienda, Ley de Arrendamientos Urbanos (LAU), regulacion de alquileres, zonas tensionadas, vivienda protegida y desahucios.

## Leyes clave

### Ley de Vivienda (BOE-A-2023-12203)

Ley 12/2023, de 24 de mayo, por el derecho a la vivienda.

| Articulo | Contenido |
|---|---|
| `a1` | Objeto de la ley |
| `a3` | Definiciones: vivienda, vivienda protegida, gran tenedor |
| `a4` | Derecho a una vivienda digna y adecuada |
| `a15` | Parque publico de vivienda |
| `a17` | Zonas de mercado residencial tensionado |
| `a18` | Declaracion de zonas de mercado tensionado |
| `a20` | Limitaciones en zona tensionada |
| `a27` | Recargos en el IBI a viviendas vacias |
| `a31` | Informacion minima en operaciones de compraventa y arrendamiento |

### LAU (BOE-A-1994-26003)

Ley 29/1994, de 24 de noviembre, de Arrendamientos Urbanos.

| Articulo | Contenido |
|---|---|
| `a1` | Ambito de aplicacion |
| `a2` | Arrendamiento de vivienda |
| `a6` | Naturaleza de las normas (imperativas) |
| `a9` | Plazo minimo (duracion del contrato) |
| `a10` | Prorroga del contrato |
| `a11` | Desistimiento del contrato |
| `a14` | Enajenacion de la vivienda arrendada |
| `a16` | Muerte del arrendatario (subrogacion) |
| `a17` | Actualizacion de la renta |
| `a18` | Fianza |
| `a20` | Gastos generales y servicios individuales |
| `a21` | Conservacion de la vivienda |
| `a27` | Extincion del contrato |

## Subtemas

- **alquiler_vivienda** -- Contratos de alquiler, duracion minima, prorrogas, actualizacion de renta, fianza
- **zonas_tensionadas** -- Limites de precio, grandes tenedores, indices de referencia, viviendas vacias
- **desahucio_proteccion** -- Procedimientos de desahucio, proteccion de inquilinos vulnerables, moratorias

## Casos de uso

```python
# Consultar duracion minima del contrato de alquiler
buscar_por_dominio("vivienda", subtema="alquiler_vivienda")

# Leer articulo sobre plazo minimo del contrato
leer_articulo("BOE-A-1994-26003", "a9")

# Verificar definicion de zona tensionada
leer_articulo("BOE-A-2023-12203", "a17")

# Consultar actualizacion de la renta
leer_articulo("BOE-A-1994-26003", "a17")
```
