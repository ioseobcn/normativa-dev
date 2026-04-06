# Agentes y skills

normativa incluye un sistema de agentes y skills para Claude Code que
automatiza consultas legales complejas y tareas de desarrollo.

## Ubicacion

```
.claude/
  agents/                  # Agentes (roles con proceso definido)
    investigador-legal.md
    extractor-articulos.md
    analista-dominio.md
    redactor-informes.md
    verificador-cumplimiento.md
    monitor-cambios.md
    dev-contributor.md
    dev-domain-builder.md
    dev-tester.md
    dev-docs-writer.md
    dev-releaser.md
  skills/                  # Skills (conocimiento cargable)
    dominio-fiscal.md
    dominio-laboral.md
    dominio-mercantil.md
    dominio-autonomos.md
    dominio-proteccion-datos.md
    dominio-digital.md
    dominio-vivienda.md
    dev-testing-patterns.md
    dev-release-process.md
    api-boe-referencia.md
  settings.json
  CLAUDE.md
```

## Agentes

### Formato YAML frontmatter

Cada agente se define en un fichero Markdown con frontmatter YAML:

```yaml
---
name: investigador-legal
description: Localiza legislacion relevante para una consulta juridica.
tools: Read, Write, ToolSearch
---
```

Campos:

| Campo | Descripcion |
|-------|-------------|
| `name` | Identificador unico del agente |
| `description` | Descripcion corta (1 linea) de su rol |
| `tools` | Lista de herramientas que puede usar (Read, Write, Edit, Bash, Grep, Glob, ToolSearch, WebSearch, WebFetch) |

### Declaracion de tools MCP

Los agentes acceden a las tools de normativa a traves del prefijo MCP:

```
mcp__normativa__buscar_legislacion
mcp__normativa__buscar_por_dominio
mcp__normativa__obtener_metadatos
mcp__normativa__obtener_analisis
mcp__normativa__leer_indice
mcp__normativa__leer_articulo
mcp__normativa__leer_articulos_rango
mcp__normativa__sumario_boe
mcp__normativa__sumario_borme
mcp__normativa__listar_dominios
mcp__normativa__datos_auxiliares
```

No todos los agentes usan todas las tools. El agente `redactor-informes`
por ejemplo NO usa tools MCP -- solo lee los archivos de handoff.

### Pipeline de agentes legales (4 fases)

```
Fase 1 (paralelo):
  investigador-legal    Localiza legislacion, verifica vigencia, mapea referencias
  monitor-cambios       Rastrea publicaciones recientes por dominio

Fase 2:
  extractor-articulos   Extrae texto literal de articulos concretos

Fase 3 (paralelo):
  analista-dominio      Interpreta legislacion con skill de dominio cargado
  verificador-cumplimiento  Contrasta situacion descrita contra requisitos legales

Fase 4:
  redactor-informes     Sintetiza todo en informe formal con citas
```

### Comunicacion via handoff/

Los agentes se comunican a traves de archivos en el directorio `handoff/`.
Cada agente produce un archivo con un slug basado en la consulta:

| Archivo | Productor | Contenido |
|---------|-----------|-----------|
| `handoff/investigacion-{slug}.md` | investigador-legal | Normas localizadas, BOE IDs, bloques a extraer |
| `handoff/extracto-{slug}.md` | extractor-articulos | Texto literal de articulos (max 10 por fichero) |
| `handoff/extracto-{slug}-2.md` | extractor-articulos | Continuacion si hay mas de 10 bloques |
| `handoff/analisis-{slug}.md` | analista-dominio | Interpretacion con citas, excepciones, trampas |
| `handoff/cumplimiento-{slug}.md` | verificador-cumplimiento | Checklist de cumplimiento con nivel de riesgo |
| `handoff/cambios-{dominio}-{fecha}.md` | monitor-cambios | Novedades legislativas detectadas |
| `handoff/informe-{slug}.md` | redactor-informes | Informe formal final |

El slug se genera a partir de la consulta del usuario
(ej: "despido-improcedente", "iva-servicios-digitales").

### Reglas comunes de los agentes

Cada agente tiene secciones `Reglas`, `Activar` y `No activar` que definen:

- **NUNCA/SIEMPRE**: restricciones absolutas (ej: "NUNCA inventes BOE IDs")
- **Activar**: cuando debe usarse este agente
- **No activar**: cuando no es el agente correcto

Reglas que aplican a todos los agentes legales:

- SIEMPRE incluir disclaimer legal en outputs que contengan interpretacion
- NUNCA inventar BOE IDs ni contenido de articulos
- NUNCA cargar leyes completas (usar `leer_indice` -> `leer_articulo`)
- Max 10 bloques por extraccion

### Detalle de cada agente

#### investigador-legal

**Fase**: 1 (entrada del pipeline)
**Rol**: Localizar legislacion, verificar vigencia, mapear referencias cruzadas.
**Tools**: `listar_dominios`, `buscar_por_dominio`, `buscar_legislacion`,
`obtener_metadatos`, `obtener_analisis`
**Output**: `handoff/investigacion-{slug}.md`
**Regla clave**: NUNCA lee articulos completos ni interpreta la ley.

#### extractor-articulos

**Fase**: 2
**Rol**: Extraer texto literal de articulos especificos.
**Tools**: `leer_indice`, `leer_articulo`, `leer_articulos_rango`
**Output**: `handoff/extracto-{slug}.md`
**Regla clave**: NUNCA modifica el texto extraido. Max 10 bloques por archivo.

#### analista-dominio

**Fase**: 3
**Rol**: Interpretar legislacion para responder consultas practicas.
**Prerrequisito**: Carga el skill de dominio relevante ANTES de analizar.
**Output**: `handoff/analisis-{slug}.md`
**Regla clave**: SIEMPRE carga el skill de dominio antes de analizar.

#### verificador-cumplimiento

**Fase**: 3 (paralelo con analista)
**Rol**: Verificar cumplimiento normativo de una situacion descrita.
**Output**: `handoff/cumplimiento-{slug}.md`
**Regla clave**: Si no hay dato para verificar un requisito, marca como
"no verificable", nunca asume cumplimiento.

#### redactor-informes

**Fase**: 4 (final)
**Rol**: Sintetizar todo en informe formal.
**Tools**: Solo Read, Write, Glob (NO usa tools MCP de normativa).
**Output**: `handoff/informe-{slug}.md`
**Regla clave**: NUNCA investiga por su cuenta. Solo trabaja con los handoff existentes.

#### monitor-cambios

**Fase**: 1 (paralelo con investigador)
**Rol**: Rastrear publicaciones recientes en BOE/BORME por dominio.
**Tools**: `sumario_boe`, `sumario_borme`, `obtener_metadatos`
**Output**: `handoff/cambios-{dominio}-{fecha}.md`
**Regla clave**: Max 30 dias por ejecucion. Cada cambio clasificado por tipo e impacto.

## Agentes de desarrollo

Para tareas de desarrollo del proyecto, no de consulta legal.

#### dev-contributor

**Rol**: Contribuir al proyecto (anadir dominios, mejorar tools, bugs).
**Tools**: Read, Write, Edit, Bash, Grep, Glob, ToolSearch
**Proceso**: Leer CLAUDE.md -> Entender patron existente -> Modificar -> Test

#### dev-domain-builder

**Rol**: Construir nuevos dominios tematicos completos.
**Tools**: Los de contributor + WebSearch, WebFetch
**Proceso**: Investigar leyes -> Verificar BOE IDs -> Crear .py -> Crear skill -> Test

#### dev-tester

**Rol**: Ejecutar y verificar tests.
**Tools**: Read, Write, Edit, Bash, Grep, Glob
**Incluye**: Tests rapidos (import check, registry check, API check) y suite completa.

#### dev-docs-writer

**Rol**: Generar y mantener documentacion.
**Proceso**: Leer source -> Extraer metadata -> Generar markdown -> Verificar con mkdocs

#### dev-releaser

**Rol**: Preparar y publicar nuevas versiones.
**Proceso**: Pre-checks -> Bump version -> CHANGELOG -> Commit/tag -> Build/publish -> GitHub release

## Skills

### Que son

Los skills son paquetes de conocimiento de dominio que los agentes cargan
bajo demanda. A diferencia de los agentes (que tienen proceso y output
definidos), los skills son **pasivos** -- contienen informacion de referencia.

### Carga lazy

Los skills NO se cargan automaticamente. Solo el agente `analista-dominio`
los carga, y solo cuando trabaja en un dominio concreto:

```
1. analista-dominio recibe consulta sobre IRPF
2. Identifica dominio: "fiscal"
3. Lee .claude/skills/dominio-fiscal.md
4. Absorbe terminologia, articulos frecuentes, trampas comunes
5. Aplica ese conocimiento al analizar los extractos
```

Esto evita cargar 8 skills de dominio en contexto cuando solo se necesita uno.

### Skills de dominio

Cada skill de dominio contiene:

| Seccion | Contenido |
|---------|-----------|
| Normativa principal | Tabla con leyes, abreviaturas y BOE IDs |
| Terminologia clave | 10+ terminos con definicion y referencia a articulo |
| Articulos mas consultados | 8+ articulos por ley, organizados por ley |
| Trampas comunes | 5+ errores frecuentes de interpretacion con realidad |
| Cross-references | Referencias cruzadas entre leyes del dominio y otros |

Ejemplo de una trampa del skill fiscal:

```markdown
### IS tipo reducido 15% para entidades de nueva creacion (art. 29.1 LIS)
- **Error**: Asumir que cualquier sociedad nueva tributa al 15%
- **Realidad**: El art. 29.1 exige que la actividad no haya sido realizada
  previamente por una persona vinculada. Si el socio era autonomo haciendo
  lo mismo, no aplica el 15%.
```

### Skills de desarrollo

| Skill | Contenido |
|-------|-----------|
| `dev-testing-patterns.md` | Patrones de test con ejemplos de codigo |
| `dev-release-process.md` | Pipeline de release paso a paso con comandos |
| `api-boe-referencia.md` | Referencia completa de las 11 tools MCP con tips |

### Crear un nuevo skill de dominio

Sigue la estructura de los skills existentes:

```markdown
# Skill: Dominio {Nombre}

## Cuando cargar
ACTIVAR cuando: analista-dominio trabaja en dominio "{slug}"
NO ACTIVAR cuando: solo se busca legislacion (usar investigador-legal)

## Normativa principal
(tabla con leyes, abreviaturas, BOE IDs)

## Terminologia clave
(10+ terminos con definicion y articulo de referencia)

## Articulos mas consultados
(organizados por ley, 8+ por ley principal)

## Trampas comunes
(5+ errores con formato Error/Realidad)

## Cross-references frecuentes
(como se conectan las leyes entre si)
```

### Crear un nuevo agente

1. Crear fichero `.claude/agents/{nombre}.md`
2. Anadir frontmatter YAML con `name`, `description`, `tools`
3. Definir secciones: Rol, Proceso (pasos numerados), Output (formato),
   Reglas (NUNCA/SIEMPRE), Activar, No activar
4. Si el agente produce output, definir la ruta en `handoff/`

## Configuracion (`settings.json`)

```json
{
  "permissions": {
    "allow": [
      "Bash(uv *)",
      "Bash(python3 *)",
      "Bash(pytest *)",
      "Bash(git *)",
      "Bash(curl -s *)",
      "Bash(mkdocs *)"
    ]
  }
}
```

Define los comandos de Bash permitidos sin confirmacion del usuario.
