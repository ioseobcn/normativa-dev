"""Dominio fiscal — IRPF, IVA, Impuesto de Sociedades, General Tributaria."""

from normativa.domains._base import DomainConfig, EURef, LeyRef, Subtema

DOMAIN = DomainConfig(
    slug="fiscal",
    nombre="Derecho Fiscal y Tributario",
    descripcion=(
        "Legislacion tributaria espanola: impuestos sobre la renta (IRPF), "
        "valor anadido (IVA), sociedades (IS) y normas generales tributarias. "
        "Cubre obligaciones fiscales de personas fisicas, juridicas y no residentes. "
        "Incluye referencias cruzadas a directivas UE transpuestas (IVA, ATAD)."
    ),
    leyes_clave={
        # ── Ley 35/2006, de 28 de noviembre, del IRPF ──
        "BOE-A-2006-20764": LeyRef(
            boe_id="BOE-A-2006-20764",
            nombre_corto="Ley IRPF",
            titulo_oficial=(
                "Ley 35/2006, de 28 de noviembre, del Impuesto sobre la Renta "
                "de las Personas Fisicas y de modificacion parcial de las leyes "
                "de los Impuestos sobre Sociedades, sobre la Renta de no "
                "Residentes y sobre el Patrimonio"
            ),
            rango="Ley",
            articulos_clave={
                "a6": "Hecho imponible",
                "a7": "Rentas exentas",
                "a17": "Rendimientos integros del trabajo",
                "a19": "Gastos deducibles de rendimientos del trabajo",
                "a20": "Reduccion por obtencion de rendimientos del trabajo",
                "a21": "Rendimientos integros del capital inmobiliario",
                "a22": "Rendimientos integros del capital mobiliario",
                "a27": "Rendimientos integros de actividades economicas",
                "a28": "Reglas generales de calculo del rendimiento neto",
                "a33": "Concepto de ganancia o perdida patrimonial",
                "a35": "Transmisiones a titulo oneroso",
                "a46": "Base liquidable general y del ahorro",
                "a63": "Tributacion familiar",
                "a68": "Deduccion por inversion en vivienda habitual (regimen transitorio)",
                "a80": "Deduccion por maternidad",
                "a96": "Obligacion de declarar",
                "a97": "Autoliquidacion",
                "a99": "Borrador de declaracion",
                "a101": "Retenciones e ingresos a cuenta",
            },
        ),
        # ── Ley 37/1992, de 28 de diciembre, del IVA ──
        "BOE-A-1992-28740": LeyRef(
            boe_id="BOE-A-1992-28740",
            nombre_corto="Ley IVA",
            titulo_oficial=(
                "Ley 37/1992, de 28 de diciembre, del Impuesto sobre el "
                "Valor Anadido"
            ),
            rango="Ley",
            articulos_clave={
                "a1": "Naturaleza del impuesto",
                "a4": "Hecho imponible",
                "a5": "Concepto de empresario o profesional",
                "a20": "Exenciones en operaciones interiores",
                "a70": "Requisitos subjetivos de la deduccion",
                "a78": "Base imponible: regla general",
                "a90": "Tipo impositivo general",
                "a91": "Tipos impositivos reducidos",
                "a92": "Tipos impositivos superreducidos",
                "a94": "Operaciones cuya realizacion origina el derecho a deducir",
                "a99": "Regla de prorrata",
                "a115": "Solicitud de devolucion al final de cada periodo de liquidacion",
                "a164": "Obligaciones formales: facturas, libros, declaraciones",
            },
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
        # ── Ley 27/2014, de 27 de noviembre, del IS ──
        "BOE-A-2014-12328": LeyRef(
            boe_id="BOE-A-2014-12328",
            nombre_corto="Ley IS",
            titulo_oficial=(
                "Ley 27/2014, de 27 de noviembre, del Impuesto sobre Sociedades"
            ),
            rango="Ley",
            articulos_clave={
                "a4": "Hecho imponible",
                "a7": "Sujeto pasivo",
                "a10": "Concepto y determinacion de la base imponible",
                "a12": "Correcciones de valor: amortizaciones",
                "a13": "Correcciones de valor: perdida por deterioro de creditos",
                "a15": "Gastos no deducibles",
                "a16": "Limitacion a la deducibilidad de gastos financieros",
                "a26": "Compensacion de bases imponibles negativas",
                "a29": "Tipo de gravamen",
                "a36": "Deduccion para evitar doble imposicion internacional",
            },
            eu_refs=[
                EURef(
                    celex="32016L1164",
                    titulo="Directiva (UE) 2016/1164 contra las practicas de elusion fiscal (ATAD)",
                    tipo="directiva",
                    eli_url="http://data.europa.eu/eli/dir/2016/1164/oj",
                    relacion="implementa",
                ),
            ],
        ),
        # ── Ley 58/2003, de 17 de diciembre, General Tributaria ──
        "BOE-A-2003-23186": LeyRef(
            boe_id="BOE-A-2003-23186",
            nombre_corto="LGT",
            titulo_oficial=(
                "Ley 58/2003, de 17 de diciembre, General Tributaria"
            ),
            rango="Ley",
            articulos_clave={
                "a2": "Concepto, fines y clases de tributos",
                "a12": "Interpretacion de normas tributarias",
                "a15": "Conflicto en la aplicacion de la norma tributaria",
                "a17": "Posicion del obligado tributario",
                "a26": "Intereses de demora",
                "a27": "Recargos por declaracion extemporanea sin requerimiento previo",
                "a34": "Derecho de los obligados tributarios",
                "a66": "Plazos de prescripcion",
                "a178": "Principio de no concurrencia de sanciones tributarias",
                "a191": "Infraccion tributaria por dejar de ingresar",
            },
        ),
    },
    subtemas=[
        Subtema(
            slug="irpf",
            nombre="IRPF",
            descripcion=(
                "Impuesto sobre la Renta de las Personas Fisicas: rendimientos "
                "del trabajo, capital, actividades economicas, ganancias "
                "patrimoniales, deducciones y obligacion de declarar."
            ),
            leyes=["BOE-A-2006-20764"],
            materias_boe=[4107, 4102],
            terminos_busqueda=[
                "IRPF", "renta personas fisicas", "declaracion renta",
                "rendimientos trabajo", "actividades economicas",
                "ganancias patrimoniales", "deducciones IRPF",
                "retencion IRPF", "modelo 100",
            ],
            casos_uso=[
                "Consultar tramos y tipos del IRPF vigentes",
                "Verificar si una renta esta exenta",
                "Calcular rendimiento neto de actividades economicas",
                "Comprobar deducciones aplicables en declaracion",
                "Determinar obligacion de presentar declaracion",
            ],
        ),
        Subtema(
            slug="iva",
            nombre="IVA",
            descripcion=(
                "Impuesto sobre el Valor Anadido: tipos impositivos, exenciones, "
                "deducciones, regimenes especiales y obligaciones formales."
            ),
            leyes=["BOE-A-1992-28740"],
            materias_boe=[4113, 4102],
            terminos_busqueda=[
                "IVA", "valor anadido", "tipo impositivo",
                "exencion IVA", "prorrata", "modelo 303",
                "facturacion", "recargo equivalencia",
                "regimen simplificado IVA",
            ],
            casos_uso=[
                "Determinar tipo de IVA aplicable a un bien o servicio",
                "Verificar si una operacion esta exenta de IVA",
                "Consultar reglas de deduccion y prorrata",
                "Comprobar obligaciones de facturacion",
            ],
        ),
        Subtema(
            slug="impuesto_sociedades",
            nombre="Impuesto de Sociedades",
            descripcion=(
                "Impuesto sobre Sociedades: base imponible, gastos deducibles, "
                "tipos de gravamen, deducciones y regimen de consolidacion fiscal."
            ),
            leyes=["BOE-A-2014-12328"],
            materias_boe=[4096, 4102],
            terminos_busqueda=[
                "impuesto sociedades", "IS", "base imponible sociedades",
                "gastos deducibles IS", "tipo gravamen sociedades",
                "modelo 200", "consolidacion fiscal",
                "compensacion bases negativas",
            ],
            casos_uso=[
                "Calcular base imponible del IS",
                "Verificar deducibilidad de un gasto",
                "Consultar tipo de gravamen aplicable",
                "Comprobar limites de compensacion de bases negativas",
            ],
        ),
        Subtema(
            slug="tributaria_general",
            nombre="Normas Generales Tributarias",
            descripcion=(
                "Ley General Tributaria: procedimientos de gestion, inspeccion, "
                "recaudacion, sanciones, prescripcion y derechos del contribuyente."
            ),
            leyes=["BOE-A-2003-23186"],
            materias_boe=[4101, 4121],
            terminos_busqueda=[
                "general tributaria", "LGT", "prescripcion tributaria",
                "sanciones tributarias", "inspeccion hacienda",
                "recargos extemporaneos", "intereses demora",
                "recurso reposicion tributario",
            ],
            casos_uso=[
                "Consultar plazos de prescripcion tributaria",
                "Verificar recargos por declaracion fuera de plazo",
                "Conocer derechos del contribuyente ante inspeccion",
                "Comprobar regimen sancionador tributario",
            ],
        ),
    ],
    materias_boe=[4107, 4102, 4113, 4101, 4096, 4121],
    departamentos_boe=["4015"],
    terminos_busqueda=[
        "fiscal", "tributario", "impuesto", "hacienda", "AEAT",
        "declaracion", "retencion", "deduccion fiscal", "exencion fiscal",
        "recargo", "sancion tributaria", "modelo tributario",
    ],
    dominios_relacionados=["autonomos", "mercantil", "laboral"],
    casos_uso={
        "declaracion_renta": "Preparar y verificar la declaracion de la renta (IRPF)",
        "facturacion_iva": "Determinar IVA aplicable y cumplir obligaciones de facturacion",
        "cierre_fiscal_empresa": "Calcular el Impuesto de Sociedades al cierre del ejercicio",
        "inspeccion_tributaria": "Conocer derechos y procedimientos ante una inspeccion de Hacienda",
        "prescripcion_deuda": "Verificar si una deuda tributaria ha prescrito",
        "recurso_sancion": "Recurrir una sancion o liquidacion tributaria",
        "planificacion_fiscal": "Optimizar la carga fiscal dentro de la legalidad",
    },
)
