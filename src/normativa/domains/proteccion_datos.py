"""Dominio proteccion de datos — LOPDGDD, derechos digitales."""

from normativa.domains._base import DomainConfig, EURef, LeyRef, Subtema

DOMAIN = DomainConfig(
    slug="proteccion_datos",
    nombre="Proteccion de Datos y Privacidad",
    descripcion=(
        "Legislacion espanola de proteccion de datos personales: LOPDGDD como "
        "complemento nacional al RGPD europeo, derechos digitales de ciudadanos "
        "y trabajadores, regimen sancionador de la AEPD. "
        "Incluye referencias cruzadas al Reglamento (UE) 2016/679 (RGPD)."
    ),
    leyes_clave={
        # ── LO 3/2018 — LOPDGDD ──
        "BOE-A-2018-16673": LeyRef(
            boe_id="BOE-A-2018-16673",
            nombre_corto="LOPDGDD",
            titulo_oficial=(
                "Ley Organica 3/2018, de 5 de diciembre, de Proteccion de Datos "
                "Personales y garantia de los derechos digitales"
            ),
            rango="Ley Organica",
            articulos_clave={
                "a4": "Deber de informar al afectado",
                "a6": "Tratamiento basado en el consentimiento del afectado",
                "a7": "Consentimiento de los menores de edad",
                "a9": "Categorias especiales de datos",
                "a12": "Disposiciones generales sobre derechos ARCO-POL",
                "a13": "Derecho de acceso",
                "a14": "Derecho de rectificacion",
                "a15": "Derecho de supresion",
                "a17": "Derecho a la portabilidad",
                "a18": "Derecho de limitacion del tratamiento",
                "a21": "Derecho de oposicion",
                "a34": "Delegado de proteccion de datos (DPO)",
                "a35": "Designacion obligatoria del DPO",
                "a36": "Posicion del DPO en la organizacion",
                "a37": "Intervencion del DPO en caso de reclamacion",
                "a40": "Regimen de responsabilidad y sanciones",
                "a44": "Medidas correctivas de la AEPD",
                "a73": "Infracciones consideradas leves",
                "a74": "Infracciones consideradas graves",
                "a75": "Infracciones consideradas muy graves",
                "a79": "Derecho a la intimidad frente al uso de dispositivos de videovigilancia",
                "a80": "Derecho a la intimidad frente al uso de sistemas de geolocalizacion",
                "a87": "Derecho a la intimidad y uso de dispositivos digitales en el ambito laboral",
                "a88": "Derecho a la desconexion digital en el ambito laboral",
                "a89": "Derecho a la intimidad frente al uso de dispositivos de videovigilancia en el lugar de trabajo",
                "a93": "Derecho al olvido en busquedas de internet",
                "a94": "Derecho al olvido en redes sociales y servicios equivalentes",
                "a96": "Derecho a la educacion digital",
            },
            eu_refs=[
                EURef(
                    celex="32016R0679",
                    titulo="Reglamento (UE) 2016/679 General de Proteccion de Datos (RGPD)",
                    tipo="reglamento",
                    eli_url="http://data.europa.eu/eli/reg/2016/679/oj",
                    relacion="complementa",
                ),
            ],
        ),
    },
    subtemas=[
        Subtema(
            slug="derechos_afectado",
            nombre="Derechos del Afectado (ARCO-POL)",
            descripcion=(
                "Derechos de acceso, rectificacion, cancelacion/supresion, "
                "oposicion, portabilidad y limitacion del tratamiento de datos "
                "personales ante responsables."
            ),
            leyes=["BOE-A-2018-16673"],
            materias_boe=[4901],
            terminos_busqueda=[
                "derecho acceso datos", "derecho rectificacion",
                "derecho supresion", "derecho olvido",
                "derecho portabilidad", "derecho oposicion",
                "ARCO", "ARCO-POL",
            ],
            casos_uso=[
                "Ejercer derecho de acceso a mis datos personales",
                "Solicitar supresion de datos (derecho al olvido)",
                "Reclamar ante la AEPD por vulneracion de derechos",
            ],
        ),
        Subtema(
            slug="obligaciones_empresas",
            nombre="Obligaciones del Responsable y Encargado",
            descripcion=(
                "Obligaciones legales de empresas que tratan datos: registro de "
                "actividades, evaluacion de impacto, notificacion de brechas, "
                "designacion de DPO y contratos de encargado."
            ),
            leyes=["BOE-A-2018-16673"],
            materias_boe=[4901],
            terminos_busqueda=[
                "responsable tratamiento", "encargado tratamiento",
                "DPO", "delegado proteccion datos",
                "registro actividades tratamiento",
                "evaluacion impacto", "brecha seguridad",
                "notificacion brecha AEPD",
            ],
            casos_uso=[
                "Determinar si necesito un DPO",
                "Elaborar registro de actividades de tratamiento",
                "Notificar una brecha de seguridad a la AEPD",
                "Redactar contrato con encargado del tratamiento",
            ],
        ),
        Subtema(
            slug="derechos_digitales",
            nombre="Derechos Digitales",
            descripcion=(
                "Derechos digitales reconocidos por la LOPDGDD: desconexion "
                "digital laboral, intimidad frente a videovigilancia y "
                "geolocalizacion, derecho al olvido en internet y redes sociales."
            ),
            leyes=["BOE-A-2018-16673"],
            materias_boe=[4901],
            terminos_busqueda=[
                "desconexion digital", "videovigilancia laboral",
                "geolocalizacion laboral", "derecho olvido internet",
                "derecho olvido redes sociales", "intimidad digital",
                "educacion digital", "testamento digital",
            ],
            casos_uso=[
                "Ejercer derecho a la desconexion digital frente al empleador",
                "Consultar limites de videovigilancia en el trabajo",
                "Solicitar derecho al olvido en Google o redes sociales",
            ],
        ),
    ],
    materias_boe=[4901],
    departamentos_boe=["4013"],
    terminos_busqueda=[
        "proteccion datos", "datos personales", "privacidad",
        "RGPD", "LOPDGDD", "AEPD", "consentimiento",
        "DPO", "delegado proteccion datos", "brecha seguridad",
        "derecho olvido", "videovigilancia",
    ],
    dominios_relacionados=["digital", "laboral"],
    casos_uso={
        "adaptacion_rgpd": "Adaptar una empresa al RGPD y la LOPDGDD",
        "ejercicio_derechos": "Ejercer derechos ARCO-POL como ciudadano",
        "brecha_seguridad": "Gestionar y notificar una brecha de datos personales",
        "dpo": "Determinar necesidad y funciones del DPO",
        "videovigilancia_legal": "Instalar camaras cumpliendo la normativa de proteccion de datos",
    },
)
