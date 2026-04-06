"""Dominio vivienda — Ley de Vivienda, LAU, arrendamientos urbanos."""

from normativa.domains._base import DomainConfig, LeyRef, Subtema

DOMAIN = DomainConfig(
    slug="vivienda",
    nombre="Derecho de la Vivienda y Arrendamientos",
    descripcion=(
        "Legislacion espanola sobre vivienda: Ley por el Derecho a la Vivienda, "
        "Ley de Arrendamientos Urbanos (LAU), regulacion de alquileres, "
        "zonas tensionadas, vivienda protegida y desahucios."
    ),
    leyes_clave={
        # ── Ley 12/2023 — Ley por el Derecho a la Vivienda ──
        "BOE-A-2023-12203": LeyRef(
            boe_id="BOE-A-2023-12203",
            nombre_corto="Ley de Vivienda",
            titulo_oficial=(
                "Ley 12/2023, de 24 de mayo, por el derecho a la vivienda"
            ),
            rango="Ley",
            articulos_clave={
                "a1": "Objeto de la ley",
                "a2": "Fines de la politica de vivienda",
                "a3": "Definiciones: vivienda, vivienda protegida, gran tenedor",
                "a4": "Derecho a una vivienda digna y adecuada",
                "a15": "Parque publico de vivienda",
                "a17": "Zonas de mercado residencial tensionado",
                "a18": "Declaracion de zonas de mercado tensionado",
                "a19": "Contenido de la declaracion de zona tensionada",
                "a20": "Limitaciones en zona de mercado residencial tensionado",
                "a27": "Recargos en el IBI a viviendas vacias",
                "a31": "Informacion minima en operaciones de compraventa y arrendamiento",
            },
        ),
        # ── Ley 29/1994 — Ley de Arrendamientos Urbanos (LAU) ──
        "BOE-A-1994-26003": LeyRef(
            boe_id="BOE-A-1994-26003",
            nombre_corto="LAU",
            titulo_oficial=(
                "Ley 29/1994, de 24 de noviembre, de Arrendamientos Urbanos"
            ),
            rango="Ley",
            articulos_clave={
                "a1": "Ambito de aplicacion",
                "a2": "Arrendamiento de vivienda",
                "a3": "Arrendamiento para uso distinto del de vivienda",
                "a4": "Regimen aplicable",
                "a6": "Naturaleza de las normas (imperativas)",
                "a7": "Condicion de vivienda habitual",
                "a9": "Plazo minimo (duracion del contrato)",
                "a10": "Prorroga del contrato",
                "a11": "Desistimiento del contrato",
                "a13": "Resolucion del derecho del arrendador",
                "a14": "Enajenacion de la vivienda arrendada",
                "a15": "Separacion, divorcio o nulidad del arrendatario",
                "a16": "Muerte del arrendatario (subrogacion)",
                "a17": "Actualizacion de la renta",
                "a18": "Fianza",
                "a20": "Gastos generales y servicios individuales",
                "a21": "Conservacion de la vivienda",
                "a23": "Obras del arrendatario",
                "a27": "Extincion del contrato de arrendamiento",
                "a36": "Fianza en arrendamiento para uso distinto de vivienda",
            },
        ),
    },
    subtemas=[
        Subtema(
            slug="alquiler_vivienda",
            nombre="Alquiler de Vivienda Habitual",
            descripcion=(
                "Contratos de alquiler de vivienda habitual: duracion minima, "
                "prorrogas, actualizacion de renta, fianza, derechos y "
                "obligaciones de arrendador y arrendatario."
            ),
            leyes=["BOE-A-1994-26003", "BOE-A-2023-12203"],
            materias_boe=[4601],
            terminos_busqueda=[
                "alquiler vivienda", "contrato alquiler",
                "duracion contrato alquiler", "prorroga alquiler",
                "fianza alquiler", "actualizacion renta",
                "IPC alquiler", "subida alquiler",
                "derechos inquilino", "derechos arrendador",
            ],
            casos_uso=[
                "Redactar contrato de alquiler de vivienda habitual",
                "Verificar duracion minima del contrato de alquiler",
                "Calcular actualizacion de la renta anual",
                "Consultar derechos del inquilino ante subida de alquiler",
                "Determinar fianza legal exigible",
            ],
        ),
        Subtema(
            slug="zonas_tensionadas",
            nombre="Zonas de Mercado Tensionado",
            descripcion=(
                "Declaracion de zonas tensionadas, limites al precio del alquiler, "
                "indice de referencia, obligaciones de grandes tenedores y "
                "recargos a viviendas vacias."
            ),
            leyes=["BOE-A-2023-12203"],
            materias_boe=[4601],
            terminos_busqueda=[
                "zona tensionada", "limite alquiler", "gran tenedor",
                "indice referencia alquiler", "vivienda vacia",
                "recargo IBI vivienda vacia", "tope alquiler",
                "control precios alquiler",
            ],
            casos_uso=[
                "Comprobar si mi municipio es zona de mercado tensionado",
                "Verificar limites al precio del alquiler en zona tensionada",
                "Consultar definicion y obligaciones de gran tenedor",
                "Determinar si aplica recargo IBI por vivienda vacia",
            ],
        ),
        Subtema(
            slug="desahucio_proteccion",
            nombre="Desahucio y Proteccion del Inquilino",
            descripcion=(
                "Procedimientos de desahucio, causas legales, proteccion de "
                "inquilinos vulnerables, moratorias y alternativas habitacionales."
            ),
            leyes=["BOE-A-1994-26003", "BOE-A-2023-12203"],
            materias_boe=[4601],
            terminos_busqueda=[
                "desahucio", "desahucio express", "lanzamiento",
                "impago alquiler", "demanda desahucio",
                "vulnerabilidad inquilino", "moratoria desahucio",
                "alternativa habitacional", "ocupacion ilegal",
            ],
            casos_uso=[
                "Conocer causas legales para iniciar un desahucio",
                "Consultar protecciones del inquilino vulnerable",
                "Verificar plazos del procedimiento de desahucio",
                "Determinar si aplica moratoria de desahucio vigente",
            ],
        ),
    ],
    materias_boe=[4601],
    departamentos_boe=["4028"],
    terminos_busqueda=[
        "vivienda", "alquiler", "arrendamiento", "LAU",
        "inquilino", "arrendatario", "arrendador", "casero",
        "contrato alquiler", "fianza", "desahucio",
        "zona tensionada", "gran tenedor", "vivienda protegida",
    ],
    dominios_relacionados=["fiscal", "proteccion_datos"],
    casos_uso={
        "contrato_alquiler": "Formalizar un contrato de alquiler conforme a la LAU",
        "subida_renta": "Verificar limites legales a la subida anual del alquiler",
        "zona_tensionada": "Comprobar regulacion aplicable en zonas de mercado tensionado",
        "desahucio_proceso": "Conocer el procedimiento legal de desahucio",
        "derechos_inquilino": "Consultar derechos y protecciones del inquilino",
    },
)
