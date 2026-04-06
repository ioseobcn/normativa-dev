# Proteccion de datos

**Proteccion de Datos y Privacidad**

Legislacion espanola de proteccion de datos personales: LOPDGDD como complemento nacional al RGPD europeo, derechos digitales de ciudadanos y trabajadores, regimen sancionador de la AEPD.

## Leyes clave

### LOPDGDD (BOE-A-2018-16673)

Ley Organica 3/2018, de 5 de diciembre, de Proteccion de Datos Personales y garantia de los derechos digitales.

| Articulo | Contenido |
|---|---|
| `a4` | Deber de informar al afectado |
| `a6` | Tratamiento basado en el consentimiento |
| `a7` | Consentimiento de los menores de edad |
| `a9` | Categorias especiales de datos |
| `a12` | Disposiciones generales sobre derechos ARCO-POL |
| `a13` | Derecho de acceso |
| `a15` | Derecho de supresion |
| `a17` | Derecho a la portabilidad |
| `a34` | Delegado de proteccion de datos (DPO) |
| `a35` | Designacion obligatoria del DPO |
| `a44` | Medidas correctivas de la AEPD |
| `a73` | Infracciones leves |
| `a74` | Infracciones graves |
| `a75` | Infracciones muy graves |
| `a87` | Intimidad y dispositivos digitales en el ambito laboral |
| `a88` | Derecho a la desconexion digital |
| `a89` | Videovigilancia en el lugar de trabajo |
| `a93` | Derecho al olvido en busquedas de internet |
| `a94` | Derecho al olvido en redes sociales |

**Referencia UE:** Complementa el [Reglamento (UE) 2016/679](http://data.europa.eu/eli/reg/2016/679/oj) General de Proteccion de Datos (RGPD).

## Subtemas

- **derechos_afectado** -- Derechos ARCO-POL: acceso, rectificacion, supresion, portabilidad, oposicion, limitacion
- **obligaciones_empresas** -- Obligaciones del responsable y encargado: DPO, registro actividades, evaluacion de impacto, brechas
- **derechos_digitales** -- Desconexion digital, videovigilancia laboral, derecho al olvido

## Casos de uso

```python
# Consultar obligaciones empresariales
buscar_por_dominio("proteccion_datos", subtema="obligaciones_empresas")

# Verificar si necesito un DPO
leer_articulo("BOE-A-2018-16673", "a34")
leer_articulo("BOE-A-2018-16673", "a35")

# Consultar regimen sancionador
leer_articulos_rango("BOE-A-2018-16673", "a73", "a75")
```
