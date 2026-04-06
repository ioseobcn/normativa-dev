# Integracion con legislacion europea

Estado actual y planes para la integracion de legislacion de la Union Europea
en normativa.

## Estado actual (v0.1)

En v0.1, la integracion EU es **declarativa**: las referencias a legislacion
europea se almacenan como metadatos en los `LeyRef` de cada dominio, pero no
hay acceso directo a los textos de EUR-Lex.

### Dataclass EURef

```python
@dataclass
class EURef:
    celex: str         # "32016R0679" (RGPD)
    titulo: str        # "Reglamento General de Proteccion de Datos"
    tipo: str          # "reglamento", "directiva", "decision"
    eli_url: str = ""  # "http://data.europa.eu/eli/reg/2016/679/oj"
    relacion: str = "transpone"  # "transpone", "implementa", "complementa", "deroga"
```

Las EURef se anidan dentro de `LeyRef`:

```python
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
```

### EU refs actuales

A fecha de v0.1, hay **5 EU refs** en **3 dominios**:

| Dominio | Ley espanola | Referencia EU | CELEX | Relacion |
|---------|-------------|---------------|-------|----------|
| fiscal | Ley IVA (BOE-A-1992-28740) | Directiva 2006/112/CE (IVA) | `32006L0112` | transpone |
| fiscal | Ley IS (BOE-A-2014-12328) | Directiva 2016/1164 (ATAD) | `32016L1164` | implementa |
| proteccion_datos | LOPDGDD (BOE-A-2018-16673) | RGPD - Reglamento 2016/679 | `32016R0679` | transpone |
| digital | LSSI (BOE-A-2002-13758) | Directiva 2000/31/CE (Comercio electronico) | `32000L0031` | transpone |
| digital | LSSI (BOE-A-2002-13758) | Directiva 2002/58/CE (ePrivacy) | `32002L0058` | transpone |

### Como se exponen via tools

Cuando una tool devuelve leyes de un dominio (via `buscar_por_dominio` o
`buscar_legislacion` con fallback al registro), las EU refs se incluyen
en el output:

```python
# En buscar_por_dominio, para cada ley con eu_refs:
entry["eu_refs"] = [
    {"celex": r.celex, "titulo": r.titulo, "tipo": r.tipo,
     "relacion": r.relacion, "eli_url": r.eli_url}
    for r in ley.eu_refs
]
```

Resultado ejemplo:

```json
{
  "boe_id": "BOE-A-1992-28740",
  "nombre_corto": "Ley IVA",
  "rango": "Ley",
  "eu_refs": [
    {
      "celex": "32006L0112",
      "titulo": "Directiva 2006/112/CE del Consejo relativa al sistema comun del IVA",
      "tipo": "directiva",
      "relacion": "transpone",
      "eli_url": "http://data.europa.eu/eli/dir/2006/112/oj"
    }
  ]
}
```

## Formato CELEX

CELEX es el sistema de identificadores de EUR-Lex. El formato para legislacion
que nos interesa:

```
Sector 3 = Legislacion
  3 + YYYY + L + NNNN = Directiva
  3 + YYYY + R + NNNN = Reglamento
  3 + YYYY + D + NNNN = Decision
```

### Ejemplos

| Acto | CELEX | Descomposicion |
|------|-------|----------------|
| RGPD | `32016R0679` | 3 (legislacion) + 2016 (ano) + R (reglamento) + 0679 (numero) |
| Directiva IVA | `32006L0112` | 3 + 2006 + L (directiva) + 0112 |
| ATAD | `32016L1164` | 3 + 2016 + L + 1164 |
| Directiva e-Commerce | `32000L0031` | 3 + 2000 + L + 0031 |
| Directiva ePrivacy | `32002L0058` | 3 + 2002 + L + 0058 |

### Como encontrar un CELEX

1. Ir a [EUR-Lex](https://eur-lex.europa.eu/)
2. Buscar el acto por titulo o numero
3. El CELEX aparece en la URL: `eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32016R0679`

## Formato ELI

ELI (European Legislation Identifier) es una URI persistente para legislacion:

```
http://data.europa.eu/eli/{tipo}/{ano}/{numero}/oj

Tipos:
  dir  = directiva
  reg  = reglamento
  dec  = decision
```

### Ejemplos

| Acto | ELI URL |
|------|---------|
| RGPD | `http://data.europa.eu/eli/reg/2016/679/oj` |
| Directiva IVA | `http://data.europa.eu/eli/dir/2006/112/oj` |
| ATAD | `http://data.europa.eu/eli/dir/2016/1164/oj` |

Las ELI URLs se resuelven a la pagina de EUR-Lex del acto en el idioma
del navegador.

## Anadir EU refs a dominios existentes

### Paso 1: Identificar la transposicion

Verificar que la ley espanola transpone realmente la directiva o implementa
el reglamento. Fuentes:

- Preambulo de la ley espanola (suele mencionar la directiva transpuesta)
- Tabla de transposicion nacional en EUR-Lex
- Portal del Ministerio correspondiente

### Paso 2: Obtener CELEX y ELI

Buscar en EUR-Lex y anotar el CELEX ID y la ELI URL.

### Paso 3: Anadir al LeyRef

```python
"BOE-A-YYYY-NNNNN": LeyRef(
    # ... campos existentes ...
    eu_refs=[
        EURef(
            celex="3YYYYLNNNN",
            titulo="Directiva (UE) YYYY/NNNN relativa a...",
            tipo="directiva",  # o "reglamento", "decision"
            eli_url="http://data.europa.eu/eli/dir/YYYY/NNNN/oj",
            relacion="transpone",  # o "implementa", "complementa"
        ),
    ],
),
```

### Paso 4: Verificar

```bash
uv run pytest tests/test_registry.py -k "eu_ref" -v
```

## Plan v0.2: Cliente CELLAR

Para la version 0.2 se planea acceso directo a los textos de EUR-Lex a traves
del servicio CELLAR de la Oficina de Publicaciones de la UE.

### CELLAR: dos interfaces

1. **SPARQL endpoint**: para queries semanticas sobre el grafo de legislacion
   ```
   https://publications.europa.eu/webapi/rdf/sparql
   ```

2. **REST API**: para obtener documentos por CELEX o ELI
   ```
   https://publications.europa.eu/resource/cellar/{cellar-id}
   ```

### Funcionalidad prevista

- `eu_metadatos(celex)` -- obtener metadatos de un acto EU
- `eu_texto(celex, articulo)` -- leer un articulo concreto
- `eu_transposiciones(celex)` -- ver que paises han transpuesto una directiva
- Enriquecimiento automatico de leyes espanolas con su legislacion EU de origen

### Fuentes de datos EUR-Lex

| Fuente | URL | Notas |
|--------|-----|-------|
| SPARQL endpoint | `https://publications.europa.eu/webapi/rdf/sparql` | Queries sobre el grafo RDF de legislacion |
| REST API | `https://publications.europa.eu/resource/cellar/` | Documentos por ID CELLAR |
| ELI resolver | `http://data.europa.eu/eli/` | Redirige a EUR-Lex |
| EUR-Lex search | `https://eur-lex.europa.eu/` | Busqueda web |
| National transposition | `https://eur-lex.europa.eu/collection/n-law.html` | Medidas nacionales de transposicion |

### Consideraciones

- CELLAR no tiene rate limiting documentado pero conviene limitar a 1-2 req/s
- Los textos de EUR-Lex estan en 24 idiomas; preferir siempre `es` (espanol)
- El formato interno es Formex (XML), similar al XML del BOE
- Se reutilizara el patron de cache SQLite con tabla `eu_textos`

## EU refs que podrian anadirse

Dominios actuales con transposiciones EU conocidas pendientes de mapear:

| Dominio | Ley espanola | Directiva/Reglamento EU | CELEX |
|---------|-------------|------------------------|-------|
| laboral | ET (BOE-A-2015-11430) | Dir. 2003/88/CE (tiempo de trabajo) | `32003L0088` |
| laboral | Ley PRL (BOE-A-1995-24292) | Dir. 89/391/CEE (seguridad en el trabajo) | `31989L0391` |
| mercantil | LSC (BOE-A-2010-10544) | Dir. 2017/1132 (sociedades) | `32017L1132` |
| vivienda | Ley credito inmobiliario | Dir. 2014/17/UE (credito hipotecario) | `32014L0017` |
| consumo | TRLGDCU | Dir. 2011/83/UE (derechos consumidores) | `32011L0083` |
| digital | -- | Reglamento DSA 2022/2065 | `32022R2065` |
| digital | -- | Reglamento DMA 2022/1925 | `32022R1925` |
| proteccion_datos | -- | Dir. 2016/680 (proteccion datos policial) | `32016L0680` |
