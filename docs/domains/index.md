# Dominios tematicos

`normativa` organiza la legislacion espanola en **dominios tematicos** que agrupan normas por area juridica. Cada dominio incluye leyes clave con articulos pre-mapeados, subtemas y terminos de busqueda optimizados.

## Dominios disponibles

| Dominio | Leyes clave | Subtemas | EU Refs |
|---|---|---|---|
| [**fiscal**](fiscal.md) | Ley IRPF, Ley IVA, Ley IS, LGT | IRPF, IVA, Impuesto Sociedades, General Tributaria | Directiva IVA, ATAD |
| [**laboral**](laboral.md) | Estatuto de los Trabajadores, LGSS, Ley PRL | Contratos, despido, Seguridad Social, prevencion | -- |
| [**mercantil**](mercantil.md) | Ley Sociedades de Capital, Codigo de Comercio | SL, SA, Registro Mercantil | -- |
| [**autonomos**](autonomos.md) | LETA, Ley IRPF, LGSS-RETA | Alta, cotizacion, fiscalidad, facturacion | -- |
| [**proteccion_datos**](proteccion-datos.md) | LOPDGDD | Derechos afectado, obligaciones empresa, derechos digitales | RGPD |
| [**digital**](digital.md) | LSSI, Ley Servicios Confianza | Comercio electronico, cookies, firma electronica | Dir. Comercio Electronico, ePrivacy |
| [**vivienda**](vivienda.md) | Ley de Vivienda, LAU | Alquiler, zonas tensionadas, desahucio | -- |

## Dominios enriquecidos vs. basicos

Los 7 dominios de la tabla son **enriquecidos**: tienen un `DomainConfig` completo con leyes mapeadas, articulos clave identificados y referencias cruzadas UE.

Ademas existen dominios **basicos** en el registro general (administrativo, penal, civil, medioambiental, tecnologia, inmobiliario, consumo) que permiten busqueda por keywords pero sin mapping de leyes concretas.

## Como anadir un nuevo dominio

1. Crear `src/normativa/domains/<nombre>.py` con un `DOMAIN = DomainConfig(...)` que defina:
   - `slug`, `nombre`, `descripcion`
   - `leyes_clave`: diccionario de `LeyRef` con BOE IDs y articulos clave
   - `subtemas`: lista de `Subtema` con terminos de busqueda y casos de uso
   - `materias_boe`, `terminos_busqueda`, `casos_uso`

2. Anadir el slug a `AVAILABLE_DOMAINS` en `src/normativa/domains/__init__.py`

3. Escribir tests en `tests/test_domain_<nombre>.py`

4. Documentar en `docs/domains/<nombre>.md`

Consulta la [guia de contribucion](../contributing.md) para detalles completos.
