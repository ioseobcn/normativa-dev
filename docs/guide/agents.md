# Agentes legales

`normativa` incluye 9 agentes especializados para Claude Code (6 legales + 3 de desarrollo) que trabajan en un pipeline de investigacion legal.

## Pipeline de investigacion

```
Fase 1 (paralelo):  investigador-legal + monitor-cambios
Fase 2:             extractor-articulos
Fase 3 (paralelo):  analista-dominio + verificador-cumplimiento
Fase 4:             redactor-informes
```

Los agentes se comunican via archivos en `handoff/`, pasando **referencias** (BOE IDs + bloque IDs) en lugar de texto completo. Esto mantiene el consumo de tokens ~12x mas eficiente que cargar leyes enteras.

## Agentes legales

### investigador-legal

**Fase 1.** Recibe la consulta del usuario y busca legislacion relevante usando `buscar_por_dominio` y `buscar_legislacion`. Identifica las normas aplicables y deja en `handoff/` la lista de BOE IDs y bloques relevantes.

### monitor-cambios

**Fase 1 (paralelo con investigador).** Consulta el sumario del BOE (`sumario_boe`) para detectar novedades legislativas recientes que puedan afectar a la consulta. Comprueba si las normas identificadas han sido modificadas recientemente.

### extractor-articulos

**Fase 2.** Recibe los BOE IDs y bloque IDs del investigador. Lee los articulos concretos usando `leer_articulo` y `leer_articulos_rango`. Extrae el texto relevante en Markdown y lo deja en `handoff/`.

### analista-dominio

**Fase 3.** Analiza los textos extraidos en el contexto del dominio juridico. Aplica el conocimiento especializado del dominio (articulos clave, subtemas, EU cross-refs) para dar una interpretacion estructurada.

### verificador-cumplimiento

**Fase 3 (paralelo con analista).** Verifica que la respuesta es consistente con la legislacion vigente. Comprueba vigencia, modificaciones recientes y coherencia entre normas citadas.

### redactor-informes

**Fase 4.** Redacta la respuesta final al usuario a partir del analisis y la verificacion. Estructura la informacion con citas a articulos concretos (BOE ID + bloque ID).

## Agentes de desarrollo

### dev-contributor

Guia para contribuir al proyecto: como anadir funcionalidad, escribir tests y seguir las convenciones del codigo.

### dev-domain-builder

Guia para crear un nuevo dominio tematico: estructura de `DomainConfig`, mapping de leyes y articulos, tests.

### dev-tester

Guia para escribir y ejecutar tests: pytest, mocking de la API del BOE, tests de dominios.

## Directorio handoff

El directorio `handoff/` es el canal de comunicacion entre agentes:

```
handoff/
  investigador-legal/     # BOE IDs y bloques relevantes
  monitor-cambios/        # Novedades legislativas detectadas
  extractor-articulos/    # Textos de articulos en Markdown
  analista-dominio/       # Analisis estructurado
  verificador/            # Resultado de verificacion
  redactor/               # Informe final
```

Cada agente lee de los directorios de agentes anteriores y escribe en el suyo.

## Ejemplo: consulta legal completa

**Consulta:** "Necesito saber las obligaciones de un autonomo que factura mas de 85.000 EUR/ano."

1. **investigador-legal** busca en dominios `autonomos` y `fiscal`, identifica la LETA, Ley IRPF, Ley IVA y LGSS-RETA
2. **monitor-cambios** verifica que no hay modificaciones recientes en las bases de cotizacion o en el umbral de IVA
3. **extractor-articulos** lee los articulos clave: LETA a1, IRPF a27-a31, IVA a164, LGSS a305-a307
4. **analista-dominio** estructura las obligaciones: alta, cotizacion RETA por ingresos reales, IVA (regimen general obligatorio), IRPF (estimacion directa), facturacion electronica
5. **verificador-cumplimiento** confirma vigencia de todos los articulos citados
6. **redactor-informes** genera la respuesta con citas normativas precisas
