"""Dominio laboral — Estatuto de los Trabajadores, Seguridad Social, PRL."""

from normativa.domains._base import DomainConfig, LeyRef, Subtema

DOMAIN = DomainConfig(
    slug="laboral",
    nombre="Derecho Laboral y Seguridad Social",
    descripcion=(
        "Legislacion laboral espanola: relaciones individuales y colectivas "
        "de trabajo, Seguridad Social, prevencion de riesgos laborales. "
        "Cubre contratos, despidos, salarios, prestaciones y cotizaciones."
    ),
    leyes_clave={
        # ── RDLeg 2/2015 — Estatuto de los Trabajadores ──
        "BOE-A-2015-11430": LeyRef(
            boe_id="BOE-A-2015-11430",
            nombre_corto="Estatuto de los Trabajadores",
            titulo_oficial=(
                "Real Decreto Legislativo 2/2015, de 23 de octubre, por el que "
                "se aprueba el texto refundido de la Ley del Estatuto de los "
                "Trabajadores"
            ),
            rango="Real Decreto Legislativo",
            articulos_clave={
                "a1": "Ambito de aplicacion",
                "a4": "Derechos laborales",
                "a8": "Forma del contrato",
                "a12": "Contrato a tiempo parcial y contrato de relevo",
                "a14": "Periodo de prueba",
                "a15": "Duracion del contrato de trabajo",
                "a26": "Del salario",
                "a27": "Salario minimo interprofesional",
                "a34": "Jornada",
                "a37": "Descanso semanal, fiestas y permisos",
                "a38": "Vacaciones anuales",
                "a39": "Movilidad funcional",
                "a41": "Modificaciones sustanciales de condiciones de trabajo",
                "a47": "Suspension del contrato",
                "a49": "Extincion del contrato",
                "a51": "Despido colectivo",
                "a52": "Extincion del contrato por causas objetivas",
                "a53": "Forma y efectos del despido por causas objetivas",
                "a54": "Despido disciplinario",
                "a55": "Forma y efectos del despido disciplinario",
                "a56": "Despido improcedente",
            },
        ),
        # ── RDLeg 8/2015 — Ley General de la Seguridad Social ──
        "BOE-A-2015-11724": LeyRef(
            boe_id="BOE-A-2015-11724",
            nombre_corto="LGSS",
            titulo_oficial=(
                "Real Decreto Legislativo 8/2015, de 30 de octubre, por el que "
                "se aprueba el texto refundido de la Ley General de la "
                "Seguridad Social"
            ),
            rango="Real Decreto Legislativo",
            articulos_clave={
                "a2": "Fines de la Seguridad Social",
                "a7": "Extension del campo de aplicacion",
                "a16": "Afiliacion, altas y bajas",
                "a19": "Bases y tipos de cotizacion",
                "a169": "Situacion legal de desempleo",
                "a172": "Periodo de cotizacion para prestacion por desempleo",
                "a204": "Condiciones generales de acceso a la jubilacion",
                "a205": "Edad de jubilacion",
                "a210": "Base reguladora de la pension de jubilacion",
                "a248": "Incapacidad temporal",
            },
        ),
        # ── Ley 31/1995 — Prevencion de Riesgos Laborales ──
        "BOE-A-1995-24292": LeyRef(
            boe_id="BOE-A-1995-24292",
            nombre_corto="Ley PRL",
            titulo_oficial=(
                "Ley 31/1995, de 8 de noviembre, de Prevencion de Riesgos "
                "Laborales"
            ),
            rango="Ley",
            articulos_clave={
                "a2": "Objeto y caracter de la norma",
                "a4": "Definiciones",
                "a14": "Derecho a la proteccion frente a riesgos laborales",
                "a15": "Principios de la accion preventiva",
                "a16": "Plan de prevencion, evaluacion de riesgos y planificacion",
                "a18": "Informacion, consulta y participacion de trabajadores",
                "a19": "Formacion de los trabajadores",
                "a22": "Vigilancia de la salud",
                "a25": "Proteccion de trabajadores especialmente sensibles",
            },
        ),
    },
    subtemas=[
        Subtema(
            slug="contratos",
            nombre="Contratos de Trabajo",
            descripcion=(
                "Tipos de contratos laborales, formalizacion, periodo de prueba, "
                "duracion, modalidades (indefinido, temporal, formacion, practicas) "
                "y conversion."
            ),
            leyes=["BOE-A-2015-11430"],
            materias_boe=[4209, 4195],
            terminos_busqueda=[
                "contrato trabajo", "contrato indefinido", "contrato temporal",
                "contrato formacion", "periodo prueba", "contrato tiempo parcial",
                "contrato practicas", "fijo discontinuo",
            ],
            casos_uso=[
                "Verificar requisitos para formalizar un contrato",
                "Consultar duracion maxima de contratos temporales",
                "Comprobar derechos en periodo de prueba",
                "Determinar conversion a contrato indefinido",
            ],
        ),
        Subtema(
            slug="despido",
            nombre="Despido y Extincion del Contrato",
            descripcion=(
                "Causas de extincion del contrato, despido disciplinario, "
                "despido objetivo, despido colectivo (ERE), indemnizaciones "
                "y procedimiento de impugnacion."
            ),
            leyes=["BOE-A-2015-11430"],
            materias_boe=[4209, 4195],
            terminos_busqueda=[
                "despido", "despido improcedente", "despido disciplinario",
                "despido objetivo", "ERE", "indemnizacion despido",
                "finiquito", "preaviso despido", "despido colectivo",
                "carta despido", "conciliacion laboral",
            ],
            casos_uso=[
                "Calcular indemnizacion por despido improcedente",
                "Verificar causas validas de despido disciplinario",
                "Consultar requisitos de forma del despido objetivo",
                "Comprobar procedimiento de ERE",
                "Determinar plazos para impugnar un despido",
            ],
        ),
        Subtema(
            slug="seguridad_social",
            nombre="Seguridad Social",
            descripcion=(
                "Regimen General de la Seguridad Social: afiliacion, cotizacion, "
                "prestaciones (desempleo, jubilacion, incapacidad temporal y "
                "permanente, maternidad/paternidad)."
            ),
            leyes=["BOE-A-2015-11724"],
            materias_boe=[4206, 4195],
            terminos_busqueda=[
                "seguridad social", "cotizacion", "jubilacion",
                "prestacion desempleo", "incapacidad temporal",
                "incapacidad permanente", "base cotizacion",
                "maternidad", "paternidad", "pension viudedad",
            ],
            casos_uso=[
                "Consultar requisitos para acceder a la jubilacion",
                "Verificar bases de cotizacion vigentes",
                "Calcular prestacion por desempleo",
                "Comprobar duracion de incapacidad temporal",
                "Determinar complementos de pensiones",
            ],
        ),
        Subtema(
            slug="prevencion_riesgos",
            nombre="Prevencion de Riesgos Laborales",
            descripcion=(
                "Obligaciones empresariales en materia de prevencion: evaluacion "
                "de riesgos, plan de prevencion, formacion, vigilancia de la "
                "salud y proteccion de trabajadores sensibles."
            ),
            leyes=["BOE-A-1995-24292"],
            materias_boe=[4204],
            terminos_busqueda=[
                "prevencion riesgos", "PRL", "evaluacion riesgos",
                "plan prevencion", "accidente laboral",
                "enfermedad profesional", "comite seguridad salud",
                "delegado prevencion", "servicio prevencion",
            ],
            casos_uso=[
                "Consultar obligaciones del empresario en PRL",
                "Verificar requisitos de evaluacion de riesgos",
                "Comprobar derechos de formacion e informacion en PRL",
                "Determinar vigilancia de la salud obligatoria",
            ],
        ),
    ],
    materias_boe=[4209, 4195, 4206, 4204],
    departamentos_boe=["4023"],
    terminos_busqueda=[
        "laboral", "trabajo", "trabajador", "empleo", "contrato",
        "despido", "salario", "jornada", "vacaciones", "convenio colectivo",
        "seguridad social", "prevencion riesgos",
    ],
    dominios_relacionados=["autonomos", "fiscal"],
    casos_uso={
        "contratacion": "Formalizar contratos laborales conforme a la ley",
        "despido_procedimiento": "Gestionar un despido cumpliendo requisitos legales",
        "calculo_indemnizacion": "Calcular indemnizaciones por despido o fin de contrato",
        "prestacion_desempleo": "Verificar derecho y calcular prestacion por desempleo",
        "jubilacion": "Comprobar requisitos y calcular pension de jubilacion",
        "accidente_laboral": "Gestionar un accidente de trabajo segun la normativa PRL",
    },
)
