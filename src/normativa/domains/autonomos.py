"""Dominio autonomos — Estatuto del Trabajo Autonomo, RETA, fiscalidad."""

from normativa.domains._base import DomainConfig, LeyRef, Subtema

DOMAIN = DomainConfig(
    slug="autonomos",
    nombre="Trabajo Autonomo y Emprendedores",
    descripcion=(
        "Legislacion del trabajo autonomo en Espana: Estatuto del Trabajo "
        "Autonomo (LETA), cotizacion al RETA, fiscalidad del autonomo "
        "(IRPF/IVA), facturacion y obligaciones formales. Dominio transversal "
        "con fiscal y laboral."
    ),
    leyes_clave={
        # ── Ley 20/2007 — Estatuto del Trabajo Autonomo (LETA) ──
        "BOE-A-2007-13409": LeyRef(
            boe_id="BOE-A-2007-13409",
            nombre_corto="LETA",
            titulo_oficial=(
                "Ley 20/2007, de 11 de julio, del Estatuto del trabajo autonomo"
            ),
            rango="Ley",
            articulos_clave={
                "a1": "Concepto y ambito subjetivo de aplicacion",
                "a3": "Derechos profesionales del trabajador autonomo",
                "a4": "Deberes profesionales basicos",
                "a5": "Derechos del TRADE (trabajador autonomo economicamente dependiente)",
                "a6": "Forma y efectos del contrato del TRADE",
                "a8": "Fuentes del regimen profesional",
                "a11": "Contratacion del TRADE",
                "a12": "Jornada y descansos del TRADE",
                "a14": "Extincion del contrato del TRADE",
                "a15": "Interrupcion justificada de la actividad profesional",
                "a16": "Prevision social y proteccion por cese de actividad",
                "a24": "Jurisdiccion competente",
                "a26": "Asociaciones profesionales de trabajadores autonomos",
            },
        ),
        # ── Referencias cruzadas (leyes de fiscal y laboral) ──
        "BOE-A-2006-20764": LeyRef(
            boe_id="BOE-A-2006-20764",
            nombre_corto="Ley IRPF (ref. autonomos)",
            titulo_oficial=(
                "Ley 35/2006, de 28 de noviembre, del Impuesto sobre la Renta "
                "de las Personas Fisicas"
            ),
            rango="Ley",
            articulos_clave={
                "a27": "Rendimientos integros de actividades economicas",
                "a28": "Reglas generales calculo rendimiento neto",
                "a30": "Estimacion directa",
                "a31": "Estimacion objetiva (modulos)",
                "a99": "Borrador de declaracion",
                "a101": "Retenciones e ingresos a cuenta",
            },
        ),
        "BOE-A-2015-11724": LeyRef(
            boe_id="BOE-A-2015-11724",
            nombre_corto="LGSS (RETA)",
            titulo_oficial=(
                "Real Decreto Legislativo 8/2015, de 30 de octubre, Ley General "
                "de la Seguridad Social — Regimen Especial de Trabajadores "
                "Autonomos"
            ),
            rango="Real Decreto Legislativo",
            articulos_clave={
                "a305": "Campo de aplicacion del RETA",
                "a306": "Afiliacion y alta en el RETA",
                "a307": "Cotizacion en el RETA",
                "a308": "Accion protectora en el RETA",
                "a327": "Prestacion por cese de actividad",
                "a329": "Requisitos para la prestacion por cese de actividad",
                "a331": "Duracion y cuantia del cese de actividad",
            },
        ),
    },
    subtemas=[
        Subtema(
            slug="alta_autonomo",
            nombre="Alta y Registro de Autonomos",
            descripcion=(
                "Tramites de alta en Hacienda (modelo 036/037) y en el RETA, "
                "eleccion de epigrafe IAE, derechos y obligaciones iniciales."
            ),
            leyes=["BOE-A-2007-13409", "BOE-A-2015-11724"],
            materias_boe=[4209, 4195],
            terminos_busqueda=[
                "alta autonomo", "modelo 036", "modelo 037",
                "alta RETA", "epigrafe IAE", "darse alta autonomo",
                "tarifa plana autonomos",
            ],
            casos_uso=[
                "Darse de alta como autonomo paso a paso",
                "Elegir epigrafe IAE correcto",
                "Verificar si aplica tarifa plana de cotizacion",
                "Consultar obligaciones tras el alta",
            ],
        ),
        Subtema(
            slug="cotizacion_reta",
            nombre="Cotizacion al RETA",
            descripcion=(
                "Bases de cotizacion por ingresos reales, cuotas, bonificaciones, "
                "tarifa plana, prestacion por cese de actividad y jubilacion "
                "del autonomo."
            ),
            leyes=["BOE-A-2015-11724", "BOE-A-2007-13409"],
            materias_boe=[4206, 4195],
            terminos_busqueda=[
                "cotizacion autonomos", "RETA", "cuota autonomos",
                "base cotizacion autonomos", "ingresos reales",
                "tarifa plana", "cese actividad autonomo",
                "jubilacion autonomo", "prestaciones RETA",
            ],
            casos_uso=[
                "Calcular cuota de autonomo por ingresos reales",
                "Verificar tramos de cotizacion vigentes",
                "Consultar requisitos de prestacion por cese de actividad",
                "Comprobar bonificaciones disponibles",
            ],
        ),
        Subtema(
            slug="fiscalidad_autonomo",
            nombre="Fiscalidad del Autonomo",
            descripcion=(
                "IRPF en actividades economicas (estimacion directa/objetiva), "
                "IVA del autonomo, retenciones, pagos fraccionados (modelo 130/131) "
                "y gastos deducibles."
            ),
            leyes=["BOE-A-2006-20764", "BOE-A-1992-28740"],
            materias_boe=[4107, 4113],
            terminos_busqueda=[
                "fiscalidad autonomo", "IRPF autonomo", "IVA autonomo",
                "gastos deducibles autonomo", "modelo 130", "modelo 131",
                "estimacion directa", "estimacion objetiva", "modulos",
                "pagos fraccionados",
            ],
            casos_uso=[
                "Determinar regimen de estimacion directa vs modulos",
                "Calcular pagos fraccionados trimestrales",
                "Verificar gastos deducibles como autonomo",
                "Consultar obligaciones trimestrales de IVA",
            ],
        ),
        Subtema(
            slug="facturacion",
            nombre="Facturacion y Obligaciones Formales",
            descripcion=(
                "Requisitos de facturacion, factura electronica, libro registro, "
                "obligaciones de informacion (modelo 347, 349) y Suministro "
                "Inmediato de Informacion (SII)."
            ),
            leyes=["BOE-A-1992-28740"],
            materias_boe=[4113, 4102],
            terminos_busqueda=[
                "facturacion autonomo", "factura electronica", "Verifactu",
                "requisitos factura", "libro registro facturas",
                "modelo 347", "modelo 349", "SII",
            ],
            casos_uso=[
                "Emitir facturas cumpliendo requisitos legales",
                "Verificar obligaciones de facturacion electronica",
                "Consultar plazos de conservacion de facturas",
                "Comprobar si debe presentar modelo 347",
            ],
        ),
    ],
    materias_boe=[4209, 4195, 4206, 4107, 4113],
    departamentos_boe=["4023", "4015"],
    terminos_busqueda=[
        "autonomo", "autonomos", "RETA", "LETA", "TRADE",
        "trabajador autonomo", "emprendedor", "freelance",
        "actividad economica", "cotizacion autonomo",
    ],
    dominios_relacionados=["fiscal", "laboral", "mercantil"],
    casos_uso={
        "alta_completa": "Realizar el alta completa como autonomo (Hacienda + RETA)",
        "cuota_mensual": "Calcular y optimizar la cuota mensual de autonomo",
        "declaracion_trimestral": "Preparar declaraciones trimestrales (IVA + IRPF)",
        "gastos_deducibles": "Determinar que gastos son deducibles como autonomo",
        "cese_actividad": "Gestionar cese de actividad y acceder a prestacion",
        "trade": "Verificar condicion y derechos del TRADE",
    },
)
