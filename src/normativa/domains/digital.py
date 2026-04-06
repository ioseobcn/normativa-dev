"""Dominio digital — LSSI, comercio electronico, servicios digitales."""

from normativa.domains._base import DomainConfig, EURef, LeyRef, Subtema

DOMAIN = DomainConfig(
    slug="digital",
    nombre="Derecho Digital y Comercio Electronico",
    descripcion=(
        "Legislacion espanola sobre sociedad de la informacion, comercio "
        "electronico, servicios digitales, firma electronica y regulacion "
        "de plataformas en linea. "
        "Incluye referencias cruzadas a directivas UE transpuestas (Comercio Electronico, ePrivacy)."
    ),
    leyes_clave={
        # ── Ley 34/2002 — LSSI-CE ──
        "BOE-A-2002-13758": LeyRef(
            boe_id="BOE-A-2002-13758",
            nombre_corto="LSSI",
            titulo_oficial=(
                "Ley 34/2002, de 11 de julio, de servicios de la sociedad de "
                "la informacion y de comercio electronico"
            ),
            rango="Ley",
            articulos_clave={
                "a5": "Deber de informacion general (aviso legal)",
                "a10": "Constancia registral del nombre de dominio",
                "a12": "Deber de retencion de datos de trafico",
                "a20": "Informacion exigida sobre comunicaciones comerciales",
                "a21": "Prohibicion de comunicaciones comerciales no solicitadas (spam)",
                "a22": "Derechos de los destinatarios de servicios",
                "a23": "Validez y eficacia de los contratos electronicos",
                "a24": "Prueba de los contratos celebrados por via electronica",
                "a27": "Obligaciones previas al inicio del procedimiento de contratacion",
                "a28": "Informacion posterior a la celebracion del contrato",
                "a38": "Infracciones",
                "a39": "Sanciones",
            },
            eu_refs=[
                EURef(
                    celex="32000L0031",
                    titulo="Directiva 2000/31/CE sobre comercio electronico",
                    tipo="directiva",
                    eli_url="http://data.europa.eu/eli/dir/2000/31/oj",
                    relacion="transpone",
                ),
                EURef(
                    celex="32002L0058",
                    titulo="Directiva 2002/58/CE sobre privacidad en comunicaciones electronicas (ePrivacy)",
                    tipo="directiva",
                    eli_url="http://data.europa.eu/eli/dir/2002/58/oj",
                    relacion="transpone",
                ),
            ],
        ),
        # ── Ley 6/2020 — Reguladora de Servicios Electronicos de Confianza ──
        "BOE-A-2020-14046": LeyRef(
            boe_id="BOE-A-2020-14046",
            nombre_corto="Ley Servicios Confianza",
            titulo_oficial=(
                "Ley 6/2020, de 11 de noviembre, reguladora de determinados "
                "aspectos de los servicios electronicos de confianza"
            ),
            rango="Ley",
            articulos_clave={
                "a1": "Objeto de la ley",
                "a3": "Firma electronica y documentos electronicos",
                "a4": "Efectos juridicos de la firma electronica",
                "a6": "Identidad y atributos de los certificados",
                "a9": "Certificados cualificados",
                "a12": "Sellos electronicos de tiempo",
                "a14": "Obligaciones de los prestadores de servicios de confianza",
            },
        ),
    },
    subtemas=[
        Subtema(
            slug="comercio_electronico",
            nombre="Comercio Electronico",
            descripcion=(
                "Obligaciones legales del comercio electronico: aviso legal, "
                "condiciones de contratacion online, informacion al consumidor "
                "y validez de contratos electronicos."
            ),
            leyes=["BOE-A-2002-13758"],
            materias_boe=[4801],
            terminos_busqueda=[
                "comercio electronico", "tienda online", "aviso legal",
                "contratacion electronica", "condiciones generales",
                "contrato a distancia", "LSSI",
            ],
            casos_uso=[
                "Redactar aviso legal conforme a la LSSI",
                "Verificar obligaciones de informacion al consumidor online",
                "Comprobar validez de un contrato celebrado por internet",
            ],
        ),
        Subtema(
            slug="comunicaciones_comerciales",
            nombre="Comunicaciones Comerciales y Cookies",
            descripcion=(
                "Regulacion de envio de comunicaciones comerciales electronicas "
                "(email marketing), cookies y consentimiento del usuario."
            ),
            leyes=["BOE-A-2002-13758"],
            materias_boe=[4801],
            terminos_busqueda=[
                "spam", "comunicaciones comerciales", "email marketing",
                "cookies", "consentimiento cookies", "newsletter legal",
                "opt-in", "opt-out",
            ],
            casos_uso=[
                "Determinar si un envio de email comercial es legal",
                "Configurar banner de cookies conforme a la normativa",
                "Consultar sanciones por envio de spam",
            ],
        ),
        Subtema(
            slug="firma_electronica",
            nombre="Firma Electronica y Servicios de Confianza",
            descripcion=(
                "Tipos de firma electronica (simple, avanzada, cualificada), "
                "certificados digitales, sellos de tiempo y prestadores de "
                "servicios de confianza."
            ),
            leyes=["BOE-A-2020-14046"],
            materias_boe=[4801],
            terminos_busqueda=[
                "firma electronica", "certificado digital", "sello electronico",
                "firma cualificada", "DNIe", "certificado FNMT",
                "prestador servicios confianza",
            ],
            casos_uso=[
                "Determinar tipo de firma electronica necesaria",
                "Verificar validez legal de un documento firmado electronicamente",
                "Consultar obligaciones de prestadores de servicios de confianza",
            ],
        ),
    ],
    materias_boe=[4801],
    departamentos_boe=["4022"],
    terminos_busqueda=[
        "digital", "internet", "comercio electronico", "LSSI",
        "servicios sociedad informacion", "firma electronica",
        "cookies", "tienda online", "ecommerce", "plataforma digital",
    ],
    dominios_relacionados=["proteccion_datos", "mercantil"],
    casos_uso={
        "tienda_online": "Cumplir requisitos legales para una tienda online",
        "politica_cookies": "Implementar politica de cookies conforme a la ley",
        "email_marketing_legal": "Enviar comunicaciones comerciales de forma legal",
        "firma_contratos": "Firmar contratos electronicamente con validez legal",
    },
)
