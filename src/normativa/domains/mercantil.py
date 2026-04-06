"""Dominio mercantil — Sociedades de Capital, Codigo de Comercio."""

from normativa.domains._base import DomainConfig, LeyRef, Subtema

DOMAIN = DomainConfig(
    slug="mercantil",
    nombre="Derecho Mercantil y Societario",
    descripcion=(
        "Legislacion mercantil espanola: sociedades de capital (SL, SA), "
        "Codigo de Comercio, registro mercantil, gobernanza corporativa "
        "y operaciones societarias."
    ),
    leyes_clave={
        # ── RDLeg 1/2010 — Ley de Sociedades de Capital ──
        "BOE-A-2010-10544": LeyRef(
            boe_id="BOE-A-2010-10544",
            nombre_corto="Ley Sociedades de Capital",
            titulo_oficial=(
                "Real Decreto Legislativo 1/2010, de 2 de julio, por el que se "
                "aprueba el texto refundido de la Ley de Sociedades de Capital"
            ),
            rango="Real Decreto Legislativo",
            articulos_clave={
                "a1": "Sociedades de capital",
                "a4": "Capital social minimo",
                "a12": "Denominacion social",
                "a20": "Escritura de constitucion",
                "a23": "Estatutos sociales",
                "a90": "Participaciones sociales y acciones",
                "a160": "Competencia de la junta general",
                "a171": "Nombramiento de administradores",
                "a190": "Deber de lealtad del administrador",
                "a204": "Accion social de responsabilidad contra administradores",
                "a225": "Deber general de diligencia",
                "a226": "Proteccion de la discrecionalidad empresarial",
                "a236": "Responsabilidad de los administradores",
                "a273": "Aplicacion del resultado",
                "a316": "Aumento de capital social",
                "a317": "Requisitos del acuerdo de aumento",
                "a343": "Reduccion de capital social",
                "a348": "Derecho de separacion",
                "a363": "Causas de disolucion",
                "a371": "Liquidacion de la sociedad",
            },
        ),
        # ── Codigo de Comercio de 1885 ──
        "BOE-A-1885-6627": LeyRef(
            boe_id="BOE-A-1885-6627",
            nombre_corto="Codigo de Comercio",
            titulo_oficial="Real Decreto de 22 de agosto de 1885, Codigo de Comercio",
            rango="Real Decreto",
            articulos_clave={
                "a1": "Concepto de comerciante",
                "a2": "Actos de comercio",
                "a16": "Registro Mercantil",
                "a22": "Contabilidad de los empresarios",
                "a25": "Libros obligatorios",
                "a34": "Presentacion de cuentas anuales",
                "a50": "Contrato de compraventa mercantil",
                "a244": "Contrato de comision mercantil",
                "a303": "Deposito mercantil",
                "a325": "Contrato de transporte terrestre",
            },
        ),
    },
    subtemas=[
        Subtema(
            slug="sociedades_limitadas",
            nombre="Sociedades de Responsabilidad Limitada (SL)",
            descripcion=(
                "Constitucion, capital social, participaciones, junta de socios, "
                "administracion, transmision de participaciones y disolucion de SL."
            ),
            leyes=["BOE-A-2010-10544"],
            materias_boe=[4311, 4301],
            terminos_busqueda=[
                "sociedad limitada", "SL", "SRL", "constitucion SL",
                "capital social SL", "participaciones sociales",
                "junta socios SL", "administrador SL",
                "transmision participaciones",
            ],
            casos_uso=[
                "Constituir una sociedad limitada",
                "Consultar derechos del socio minoritario en SL",
                "Verificar obligaciones del administrador de SL",
                "Transmitir participaciones sociales",
                "Disolver y liquidar una SL",
            ],
        ),
        Subtema(
            slug="sociedades_anonimas",
            nombre="Sociedades Anonimas (SA)",
            descripcion=(
                "Constitucion, acciones, junta general de accionistas, consejo "
                "de administracion, ampliaciones de capital y obligaciones de "
                "transparencia de SA."
            ),
            leyes=["BOE-A-2010-10544"],
            materias_boe=[4311, 4301],
            terminos_busqueda=[
                "sociedad anonima", "SA", "acciones", "junta accionistas",
                "consejo administracion", "ampliacion capital",
                "derecho suscripcion preferente",
            ],
            casos_uso=[
                "Constituir una sociedad anonima",
                "Convocar junta general de accionistas",
                "Realizar una ampliacion de capital",
                "Consultar responsabilidad del consejo de administracion",
            ],
        ),
        Subtema(
            slug="registro_mercantil",
            nombre="Registro Mercantil y Contabilidad",
            descripcion=(
                "Obligaciones registrales y contables: inscripcion en Registro "
                "Mercantil, libros de comercio, cuentas anuales y deposito."
            ),
            leyes=["BOE-A-1885-6627", "BOE-A-2010-10544"],
            materias_boe=[4301],
            terminos_busqueda=[
                "registro mercantil", "cuentas anuales", "deposito cuentas",
                "libros contabilidad", "balance", "memoria anual",
                "legalizar libros",
            ],
            casos_uso=[
                "Inscribir una sociedad en el Registro Mercantil",
                "Depositar cuentas anuales",
                "Consultar obligaciones contables del empresario",
                "Legalizar libros de contabilidad",
            ],
        ),
    ],
    materias_boe=[4311, 4301],
    departamentos_boe=["4013"],
    terminos_busqueda=[
        "mercantil", "societario", "sociedad", "empresa", "comercio",
        "administrador", "junta general", "capital social", "cuentas anuales",
        "registro mercantil",
    ],
    dominios_relacionados=["fiscal", "autonomos"],
    casos_uso={
        "constitucion_sociedad": "Crear una SL o SA cumpliendo requisitos legales",
        "gobernanza_societaria": "Gestionar organos de gobierno: junta, administradores",
        "responsabilidad_administrador": "Conocer deberes y responsabilidad del administrador",
        "operacion_societaria": "Ampliaciones, reducciones de capital, fusiones, escisiones",
        "disolucion_liquidacion": "Disolver y liquidar una sociedad de capital",
    },
)
