# Crear dominios tematicos

Guia completa para crear un nuevo dominio en normativa. Seguiremos el ejemplo
del dominio `fiscal` como referencia.

## Que es un dominio

Un dominio agrupa legislacion por area juridica (fiscal, laboral, mercantil...).
Cada dominio define:

- **Leyes clave** con sus BOE IDs verificados y articulos de referencia
- **Subtemas** con terminos de busqueda y casos de uso
- **Materias BOE** (codigos numericos internos del BOE)
- **EU refs** (legislacion europea transpuesta, si aplica)

Esto permite que un LLM localice legislacion precisa sin conocer la
nomenclatura del BOE.

## Paso 1: Investigacion

Antes de escribir codigo, identifica las leyes fundamentales del dominio.

### 1.1 Identificar leyes principales

Cada dominio tiene 2-4 leyes fundamentales. Busca:

- La ley organica o ley ordinaria principal del area
- Los reglamentos de desarrollo mas importantes
- Normativa transversal que afecta al dominio

Ejemplo para un hipotetico dominio `procesal_civil`:

- Ley 1/2000, de Enjuiciamiento Civil (LEC)
- Ley Organica 6/1985, del Poder Judicial (LOPJ)
- Ley 1/1996, de Asistencia Juridica Gratuita

### 1.2 Verificar BOE IDs

Cada ley tiene un BOE ID unico. Verificalo con curl:

```bash
curl -s -H "Accept: application/json" \
  "https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/BOE-A-2000-323/metadatos" \
  | python3 -m json.tool
```

Si devuelve metadatos con `estado_consolidacion: "Vigente"`, el ID es correcto.
Si devuelve 404, busca el ID correcto en [boe.es](https://www.boe.es/).

### 1.3 Obtener indice de articulos

Para cada ley, obtiene el indice para mapear articulos clave:

```bash
curl -s -H "Accept: application/json" \
  "https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/BOE-A-2000-323/texto/indice" \
  | python3 -m json.tool
```

Selecciona 8-15 articulos clave por ley: los mas consultados, los que definen
conceptos fundamentales, y los que tienen aplicacion practica directa.

### 1.4 Obtener materias BOE

```bash
curl -s -H "Accept: application/json" \
  "https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/BOE-A-2000-323/analisis" \
  | python3 -m json.tool
```

Busca el campo `materias` en la respuesta. Los codigos de materia se usan
en el campo `materias_boe` del dominio y los subtemas.

## Paso 2: Crear el modulo Python

Crea el fichero `src/normativa/domains/{slug}.py`.

### Template completo

```python
"""Dominio {nombre} -- {descripcion corta}."""

from normativa.domains._base import DomainConfig, EURef, LeyRef, Subtema

DOMAIN = DomainConfig(
    slug="{slug}",
    nombre="{Nombre Completo del Dominio}",
    descripcion=(
        "{Descripcion de 2-3 lineas que explique que cubre este dominio. "
        "Incluye las leyes principales, los temas que abarca y a quien afecta.}"
    ),
    leyes_clave={
        # -- Ley X/YYYY, de DD de mes, titulo --
        "BOE-A-YYYY-NNNNN": LeyRef(
            boe_id="BOE-A-YYYY-NNNNN",
            nombre_corto="{Abreviatura comun}",
            titulo_oficial=(
                "{Titulo oficial completo de la ley tal como aparece en el BOE}"
            ),
            rango="{Ley|Ley Organica|Real Decreto|Real Decreto Legislativo}",
            articulos_clave={
                "a1": "Objeto de la ley",
                "a2": "Ambito de aplicacion",
                # ... 8-15 articulos clave
            },
            eu_refs=[
                # Solo si esta ley transpone legislacion EU
                EURef(
                    celex="3YYYYLNNNN",
                    titulo="Directiva (UE) YYYY/NNNN relativa a...",
                    tipo="directiva",
                    eli_url="http://data.europa.eu/eli/dir/YYYY/NNNN/oj",
                    relacion="transpone",
                ),
            ],
        ),
        # Repetir para cada ley clave (2-4 leyes por dominio)
    },
    subtemas=[
        Subtema(
            slug="{subtema_slug}",
            nombre="{Nombre del Subtema}",
            descripcion=(
                "{Descripcion de 1-2 lineas de lo que cubre este subtema.}"
            ),
            leyes=["BOE-A-YYYY-NNNNN"],  # BOE IDs de leyes aplicables
            materias_boe=[1234, 5678],     # Codigos de materia del BOE
            terminos_busqueda=[
                "{termino1}", "{termino2}", "{termino3}",
                # 8-10 terminos que un usuario usaria para buscar este tema
            ],
            casos_uso=[
                "Consultar X vigente",
                "Verificar si Y cumple con Z",
                # 3-5 casos de uso practicos
            ],
        ),
        # Repetir para 3-5 subtemas
    ],
    materias_boe=[1234, 5678, 9012],  # Union de todas las materias de los subtemas
    departamentos_boe=["4015"],        # Codigos de departamentos emisores
    terminos_busqueda=[
        # 10-15 terminos generales del dominio
        "{termino1}", "{termino2}", "{termino3}",
    ],
    dominios_relacionados=["{otro_dominio1}", "{otro_dominio2}"],
    casos_uso={
        "{caso_slug}": "{Descripcion del caso de uso}",
        # 5-7 casos de uso clave del dominio
    },
)
```

### Ejemplo real: extracto de fiscal.py

```python
DOMAIN = DomainConfig(
    slug="fiscal",
    nombre="Derecho Fiscal y Tributario",
    descripcion=(
        "Legislacion tributaria espanola: impuestos sobre la renta (IRPF), "
        "valor anadido (IVA), sociedades (IS) y normas generales tributarias."
    ),
    leyes_clave={
        "BOE-A-2006-20764": LeyRef(
            boe_id="BOE-A-2006-20764",
            nombre_corto="Ley IRPF",
            titulo_oficial=(
                "Ley 35/2006, de 28 de noviembre, del Impuesto sobre la Renta "
                "de las Personas Fisicas..."
            ),
            rango="Ley",
            articulos_clave={
                "a6": "Hecho imponible",
                "a7": "Rentas exentas",
                "a17": "Rendimientos integros del trabajo",
                "a96": "Obligacion de declarar",
                # ...
            },
        ),
        "BOE-A-1992-28740": LeyRef(
            boe_id="BOE-A-1992-28740",
            nombre_corto="Ley IVA",
            # ...
            eu_refs=[
                EURef(
                    celex="32006L0112",
                    titulo="Directiva 2006/112/CE del Consejo relativa al sistema comun del IVA",
                    tipo="directiva",
                    eli_url="http://data.europa.eu/eli/dir/2006/112/oj",
                    relacion="transpone",
                ),
            ],
        ),
    },
    subtemas=[
        Subtema(
            slug="irpf",
            nombre="IRPF",
            descripcion="Impuesto sobre la Renta de las Personas Fisicas...",
            leyes=["BOE-A-2006-20764"],
            materias_boe=[4107, 4102],
            terminos_busqueda=[
                "IRPF", "renta personas fisicas", "declaracion renta",
                "rendimientos trabajo", "deducciones IRPF",
            ],
            casos_uso=[
                "Consultar tramos y tipos del IRPF vigentes",
                "Verificar si una renta esta exenta",
            ],
        ),
    ],
    # ...
)
```

## Paso 3: Anadir EU refs (si aplica)

Si las leyes del dominio transponen directivas europeas o implementan
reglamentos EU, anade `eu_refs` al `LeyRef` correspondiente.

### Formato CELEX

Los IDs CELEX siguen este patron:

| Tipo | Formato | Ejemplo |
|------|---------|---------|
| Directiva | `3YYYYLNNNN` | `32006L0112` (Directiva IVA) |
| Reglamento | `3YYYYRNNNN` | `32016R0679` (RGPD) |
| Decision | `3YYYYDNNNN` | `32010D0087` |

### Formato ELI URL

```
http://data.europa.eu/eli/{tipo}/{ano}/{numero}/oj

Ejemplos:
http://data.europa.eu/eli/dir/2006/112/oj       (directiva)
http://data.europa.eu/eli/reg/2016/679/oj        (reglamento)
```

### Tipos de relacion

- `transpone`: ley nacional que incorpora una directiva UE al ordenamiento interno
- `implementa`: ley que desarrolla un reglamento UE (complementa su aplicacion)
- `complementa`: normativa nacional complementaria a legislacion EU
- `deroga`: norma EU derogada por otra posterior

Solo anade refs que puedas confirmar (consulta EUR-Lex si es necesario).

## Paso 4: Registrar en AVAILABLE_DOMAINS

Edita `src/normativa/domains/__init__.py` y anade el slug a la lista:

```python
AVAILABLE_DOMAINS: list[str] = [
    "fiscal",
    "laboral",
    "mercantil",
    "autonomos",
    "proteccion_datos",
    "digital",
    "vivienda",
    "{tu_nuevo_dominio}",  # <-- Anadir aqui
]
```

Si el dominio ya existe en `DOMINIOS` como diccionario simple, no necesitas
modificar `DOMINIOS`. El sistema cargara automaticamente el `DomainConfig`
enriquecido desde el fichero .py.

## Paso 5: Crear skill para agentes

Crea `.claude/skills/dominio-{slug}.md` siguiendo el patron de los skills
existentes.

### Template de skill

```markdown
# Skill: Dominio {Nombre}

## Cuando cargar
ACTIVAR cuando: analista-dominio trabaja en dominio "{slug}"
NO ACTIVAR cuando: solo se busca legislacion (usar investigador-legal)

## Normativa principal

| Ley | Abreviatura | BOE |
|-----|-------------|-----|
| {Titulo completo} | {SIGLA} | {BOE-A-YYYY-NNNNN} |

## Terminologia clave

- **{Termino}**: {Definicion con referencia a articulo} (art. X {SIGLA})

## Articulos mas consultados

### {Ley 1} -- {Titulo} (BOE-A-YYYY-NNNNN)
1. **art. X**: {Descripcion del contenido}
2. **art. Y**: {Descripcion}

## Trampas comunes

### {Titulo de la trampa} (art. X {SIGLA})
- **Error**: {Lo que la gente asume incorrectamente}
- **Realidad**: {Lo que dice la ley realmente}

## Cross-references frecuentes

- {SIGLA1} art. X -> remite a {SIGLA2} art. Y para {motivo}
```

El skill debe incluir:

- 10+ terminos con definicion y referencia a articulo
- Articulos mas consultados organizados por ley (8+ por ley principal)
- 5+ trampas comunes (errores frecuentes de interpretacion)
- Cross-references entre leyes del dominio y con otros dominios

## Paso 6: Crear pagina de documentacion

Crea `docs/domains/{slug}.md` con la documentacion orientada al usuario:

```markdown
# {Nombre del Dominio}

{Descripcion}

## Leyes incluidas

| Ley | BOE ID | Articulos clave |
|-----|--------|----------------|
| {nombre} | {BOE-ID} | {N} articulos |

## Subtemas

### {Subtema 1}

{Descripcion}

**Casos de uso:**
- {caso 1}
- {caso 2}

## Ejemplos de consulta

```
buscar_por_dominio(dominio="{slug}", subtema="{sub}")
```

## Legislacion EU relacionada

| Directiva/Reglamento | CELEX | Relacion |
|---------------------|-------|----------|
| {titulo} | {celex} | {transpone/implementa} |
```

Anade la pagina al `nav` en `mkdocs.yml`.

## Paso 7: Verificar con tests

### Verificacion rapida

```bash
# Verificar que carga correctamente
uv run python -c "
from normativa.registry import load_domain
d = load_domain('{slug}')
print(f'{d.nombre}: {len(d.leyes_clave)} leyes, {len(d.subtemas)} subtemas')
for boe_id, ley in d.leyes_clave.items():
    print(f'  {boe_id}: {ley.nombre_corto} ({len(ley.articulos_clave)} arts)')
"
```

### Tests automaticos

Los tests existentes en `test_registry.py` verifican automaticamente los
dominios nuevos:

- `test_all_available_domains_load` -- verifica que todos los slugs en
  `AVAILABLE_DOMAINS` cargan sin error
- `test_all_available_domains_listed` -- verifica que aparecen en
  `list_domains()`

Anade tests especificos para tu dominio:

```python
# tests/test_registry.py

def test_{slug}_loads(self):
    cfg = load_domain("{slug}")
    assert cfg.slug == "{slug}"
    assert len(cfg.leyes_clave) >= 2

def test_{slug}_has_subtemas(self):
    cfg = load_domain("{slug}")
    assert len(cfg.subtemas) >= 3
```

Si el dominio tiene EU refs, anade tambien:

```python
def test_{slug}_has_eu_refs(self):
    cfg = load_domain("{slug}")
    eu_ref_count = sum(len(ley.eu_refs) for ley in cfg.leyes_clave.values())
    assert eu_ref_count >= 1
```

### Suite completa

```bash
uv run pytest -v
```

## Checklist final

- [ ] Fichero `src/normativa/domains/{slug}.py` creado con `DOMAIN = DomainConfig(...)`
- [ ] Todos los BOE IDs verificados con curl (devuelven metadatos)
- [ ] 2-4 leyes clave con 8-15 articulos cada una
- [ ] 3-5 subtemas con terminos de busqueda y casos de uso
- [ ] EU refs anadidas si hay transposicion
- [ ] Slug anadido a `AVAILABLE_DOMAINS` en `domains/__init__.py`
- [ ] Skill creado en `.claude/skills/dominio-{slug}.md`
- [ ] Pagina de docs creada en `docs/domains/{slug}.md`
- [ ] `mkdocs.yml` actualizado con la nueva pagina
- [ ] `uv run pytest -v` pasa sin errores
- [ ] Verificacion manual con `load_domain("{slug}")` funciona
