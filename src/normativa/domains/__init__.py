"""Registro de dominios tematicos para legislacion espanola."""

from __future__ import annotations

from typing import Any

# Dominios con DomainConfig completo (leyes, articulos_clave, subtemas tipados)
AVAILABLE_DOMAINS: list[str] = [
    "fiscal",
    "laboral",
    "mercantil",
    "autonomos",
    "proteccion_datos",
    "digital",
    "vivienda",
]

# ---------------------------------------------------------------------------
# Registro de dominios tematicos
#
# Cada dominio agrupa terminos de busqueda, materias BOE y rangos tipicos
# que permiten al LLM hacer consultas precisas sin que el usuario tenga
# que conocer la nomenclatura del BOE.
# ---------------------------------------------------------------------------

DOMINIOS: dict[str, dict[str, Any]] = {
    "laboral": {
        "nombre": "Derecho Laboral y Seguridad Social",
        "descripcion": "Estatuto de los Trabajadores, convenios colectivos, Seguridad Social, prevencion de riesgos, EREs, contratos de trabajo.",
        "keywords": [
            "trabajadores", "laboral", "empleo", "convenio colectivo",
            "seguridad social", "prevencion riesgos", "despido", "contrato trabajo",
            "salario", "jornada", "vacaciones", "incapacidad", "prestaciones",
        ],
        "materias_boe": ["Empleo", "Trabajo", "Seguridad Social"],
        "rangos_tipicos": ["Ley Organica", "Ley", "Real Decreto-ley", "Real Decreto"],
        "subtemas": {
            "contratos": "Tipos de contrato, temporalidad, fijo-discontinuo",
            "despido": "Despido objetivo, disciplinario, colectivo, ERE",
            "seguridad_social": "Cotizaciones, prestaciones, jubilacion, IT",
            "prevencion": "Prevencion de riesgos laborales, salud laboral",
            "convenios": "Convenios colectivos sectoriales y de empresa",
        },
    },
    "fiscal": {
        "nombre": "Derecho Fiscal y Tributario",
        "descripcion": "IRPF, IVA, Impuesto de Sociedades, LGT, procedimientos tributarios, sanciones fiscales.",
        "keywords": [
            "impuesto", "tributario", "fiscal", "IRPF", "IVA", "sociedades",
            "hacienda", "contribuyente", "deduccion", "exencion", "retencion",
            "autoliquidacion", "inspeccion tributaria", "sancion tributaria",
        ],
        "materias_boe": ["Impuestos", "Hacienda Publica", "Tributos"],
        "rangos_tipicos": ["Ley", "Real Decreto-ley", "Real Decreto", "Orden"],
        "subtemas": {
            "irpf": "Impuesto sobre la Renta de las Personas Fisicas",
            "iva": "Impuesto sobre el Valor Anadido",
            "sociedades": "Impuesto sobre Sociedades",
            "procedimiento": "Procedimientos tributarios, inspeccion, recaudacion",
            "local": "Tributos locales, IBI, plusvalia, tasas",
        },
    },
    "mercantil": {
        "nombre": "Derecho Mercantil y Societario",
        "descripcion": "Ley de Sociedades de Capital, concursal, competencia, propiedad industrial, marcas.",
        "keywords": [
            "sociedades", "mercantil", "empresa", "concursal", "quiebra",
            "competencia", "marca", "patente", "comercio", "registro mercantil",
            "administrador", "junta general", "accionista", "fusion", "escision",
        ],
        "materias_boe": ["Comercio", "Empresa", "Propiedad Industrial"],
        "rangos_tipicos": ["Ley", "Real Decreto-ley", "Real Decreto"],
        "subtemas": {
            "sociedades": "SA, SL, constitucion, organos sociales",
            "concursal": "Concurso de acreedores, reestructuracion",
            "competencia": "Defensa de la competencia, competencia desleal",
            "propiedad_industrial": "Marcas, patentes, disenos",
        },
    },
    "autonomos": {
        "nombre": "Trabajo Autonomo y Emprendedores",
        "descripcion": "LETA, cotizacion RETA, fiscalidad del autonomo, facturacion, TRADE.",
        "keywords": [
            "autonomo", "autonomos", "RETA", "LETA", "TRADE",
            "trabajador autonomo", "emprendedor", "freelance",
            "cotizacion autonomo", "cuota autonomo", "modelo 036",
        ],
        "materias_boe": ["Empleo", "Trabajo", "Impuestos"],
        "rangos_tipicos": ["Ley", "Real Decreto-ley", "Real Decreto"],
        "subtemas": {
            "alta_autonomo": "Alta en Hacienda y RETA, tramites iniciales",
            "cotizacion_reta": "Bases de cotizacion, cuotas, tarifa plana",
            "fiscalidad_autonomo": "IRPF, IVA, modelos trimestrales",
            "facturacion": "Facturacion, Verifactu, obligaciones formales",
        },
    },
    "administrativo": {
        "nombre": "Derecho Administrativo",
        "descripcion": "Procedimiento administrativo, contratacion publica, expropiacion, responsabilidad patrimonial.",
        "keywords": [
            "administrativo", "procedimiento", "contratacion publica", "licitacion",
            "administracion", "funcionario", "expropiacion", "recurso",
            "subvencion", "silencio administrativo", "responsabilidad patrimonial",
        ],
        "materias_boe": ["Administracion Publica", "Funcion Publica", "Contratacion Administrativa"],
        "rangos_tipicos": ["Ley", "Ley Organica", "Real Decreto"],
        "subtemas": {
            "procedimiento": "LPAC, procedimiento administrativo comun",
            "contratacion": "Contratos del sector publico, licitaciones",
            "funcion_publica": "Empleo publico, oposiciones, funcionarios",
            "subvenciones": "Ley General de Subvenciones",
            "urbanismo": "Suelo, ordenacion territorial, licencias",
        },
    },
    "penal": {
        "nombre": "Derecho Penal",
        "descripcion": "Codigo Penal, LECrim, delitos, penas, medidas de seguridad.",
        "keywords": [
            "penal", "delito", "pena", "codigo penal", "prision",
            "multa", "lecrim", "enjuiciamiento criminal", "victima",
            "violencia genero", "ciberdelito", "blanqueo", "estafa",
        ],
        "materias_boe": ["Derecho Penal", "Justicia"],
        "rangos_tipicos": ["Ley Organica", "Ley"],
        "subtemas": {
            "codigo_penal": "Parte general y especial del CP",
            "procesal": "LECrim, procedimiento penal",
            "violencia_genero": "Proteccion integral contra violencia de genero",
            "menores": "Responsabilidad penal del menor",
        },
    },
    "civil": {
        "nombre": "Derecho Civil",
        "descripcion": "Codigo Civil, contratos, familia, sucesiones, propiedad, hipotecario.",
        "keywords": [
            "civil", "contrato", "obligacion", "propiedad", "herencia",
            "familia", "divorcio", "matrimonio", "hipoteca", "arrendamiento",
            "responsabilidad civil", "tutela", "menores", "adopcion",
        ],
        "materias_boe": ["Derecho Civil", "Registro Civil", "Propiedad"],
        "rangos_tipicos": ["Ley", "Ley Organica", "Real Decreto-ley"],
        "subtemas": {
            "familia": "Matrimonio, divorcio, filiacion, custodia",
            "sucesiones": "Herencias, testamentos, legitimas",
            "contratos": "Obligaciones y contratos civiles",
            "propiedad": "Derechos reales, propiedad horizontal, hipotecario",
            "arrendamientos": "LAU, arrendamientos urbanos y rusticos",
        },
    },
    "proteccion_datos": {
        "nombre": "Proteccion de Datos y Privacidad",
        "descripcion": "LOPDGDD, RGPD, derechos digitales, transferencias internacionales.",
        "keywords": [
            "proteccion datos", "privacidad", "RGPD", "LOPDGDD",
            "datos personales", "consentimiento", "delegado proteccion datos",
            "brecha seguridad", "derecho olvido", "videovigilancia",
        ],
        "materias_boe": ["Proteccion de Datos"],
        "rangos_tipicos": ["Ley Organica", "Real Decreto"],
        "subtemas": {
            "derechos": "ARCO, portabilidad, limitacion, supresion",
            "empresas": "Obligaciones para responsables y encargados",
            "digital": "Derechos digitales, desconexion digital",
        },
    },
    "digital": {
        "nombre": "Derecho Digital y Comercio Electronico",
        "descripcion": "LSSI, firma electronica, comercio electronico, servicios digitales, cookies.",
        "keywords": [
            "digital", "internet", "comercio electronico", "LSSI",
            "firma electronica", "cookies", "tienda online", "ecommerce",
            "certificado digital", "plataforma digital",
        ],
        "materias_boe": ["Telecomunicaciones", "Tecnologia"],
        "rangos_tipicos": ["Ley", "Ley Organica", "Real Decreto", "Real Decreto-ley"],
        "subtemas": {
            "comercio_electronico": "LSSI, tiendas online, contratacion electronica",
            "comunicaciones_comerciales": "Spam, cookies, email marketing",
            "firma_electronica": "Firma electronica, certificados, servicios de confianza",
        },
    },
    "vivienda": {
        "nombre": "Derecho de la Vivienda y Arrendamientos",
        "descripcion": "Ley de Vivienda, LAU, arrendamientos urbanos, zonas tensionadas, desahucios.",
        "keywords": [
            "vivienda", "alquiler", "arrendamiento", "LAU",
            "inquilino", "arrendatario", "arrendador", "casero",
            "contrato alquiler", "fianza", "desahucio",
            "zona tensionada", "gran tenedor", "vivienda protegida",
        ],
        "materias_boe": ["Vivienda", "Urbanismo", "Propiedad"],
        "rangos_tipicos": ["Ley", "Real Decreto-ley", "Real Decreto"],
        "subtemas": {
            "alquiler_vivienda": "Contratos de alquiler, duracion, renta, fianza",
            "zonas_tensionadas": "Limites de precio, grandes tenedores, indices",
            "desahucio_proteccion": "Desahucios, proteccion inquilinos vulnerables",
        },
    },
    "medioambiental": {
        "nombre": "Derecho Medioambiental",
        "descripcion": "Evaluacion ambiental, residuos, aguas, costas, cambio climatico, biodiversidad.",
        "keywords": [
            "medioambiente", "ambiental", "residuos", "aguas", "costas",
            "contaminacion", "evaluacion ambiental", "biodiversidad",
            "cambio climatico", "emisiones", "energia renovable", "parque natural",
        ],
        "materias_boe": ["Medio Ambiente", "Aguas", "Costas"],
        "rangos_tipicos": ["Ley", "Real Decreto", "Real Decreto-ley"],
        "subtemas": {
            "evaluacion": "Evaluacion de impacto ambiental, autorizacion ambiental",
            "residuos": "Gestion de residuos, economia circular",
            "aguas": "Dominio publico hidraulico, vertidos, depuracion",
            "clima": "Cambio climatico, transicion energetica",
        },
    },
    "tecnologia": {
        "nombre": "Derecho Digital y Tecnologico",
        "descripcion": "LSSI, firma electronica, IA, ciberseguridad, telecomunicaciones, comercio electronico.",
        "keywords": [
            "digital", "tecnologia", "telecomunicaciones", "internet",
            "firma electronica", "ciberseguridad", "inteligencia artificial",
            "comercio electronico", "LSSI", "ENS", "certificado digital",
        ],
        "materias_boe": ["Telecomunicaciones", "Tecnologia"],
        "rangos_tipicos": ["Ley", "Ley Organica", "Real Decreto", "Real Decreto-ley"],
        "subtemas": {
            "ia": "Inteligencia artificial, algoritmos, transparencia algoritmica",
            "ciberseguridad": "ENS, NIS2, seguridad redes",
            "ecommerce": "Comercio electronico, LSSI, servicios digitales",
            "telecomunicaciones": "Regulacion teleco, espectro, operadores",
        },
    },
    "inmobiliario": {
        "nombre": "Derecho Inmobiliario y Urbanismo",
        "descripcion": "Ley de Suelo, arrendamientos urbanos, propiedad horizontal, vivienda, catastro.",
        "keywords": [
            "inmobiliario", "vivienda", "suelo", "urbanismo", "propiedad horizontal",
            "arrendamiento", "alquiler", "catastro", "registro propiedad",
            "hipoteca", "VPO", "rehabilitacion", "licencia urbanistica",
        ],
        "materias_boe": ["Vivienda", "Urbanismo", "Propiedad"],
        "rangos_tipicos": ["Ley", "Real Decreto-ley", "Real Decreto"],
        "subtemas": {
            "vivienda": "Ley de Vivienda, VPO, alquiler social",
            "arrendamientos": "LAU, limites renta, zonas tensionadas",
            "urbanismo": "Planeamiento, licencias, disciplina urbanistica",
            "hipotecario": "Ley Hipotecaria, ejecucion hipotecaria",
        },
    },
    "consumo": {
        "nombre": "Derecho del Consumo",
        "descripcion": "Proteccion consumidores, garantias, clausulas abusivas, publicidad, product liability.",
        "keywords": [
            "consumidor", "consumo", "garantia", "clausula abusiva",
            "publicidad", "reclamacion", "producto defectuoso",
            "desistimiento", "condiciones generales", "arbitraje consumo",
        ],
        "materias_boe": ["Consumidores", "Comercio"],
        "rangos_tipicos": ["Ley", "Real Decreto-ley", "Real Decreto"],
        "subtemas": {
            "garantias": "Garantias de bienes de consumo",
            "clausulas": "Clausulas abusivas, condiciones generales",
            "publicidad": "Publicidad, competencia desleal, influencers",
            "reclamaciones": "Hojas de reclamacion, arbitraje, mediacion",
        },
    },
}


def buscar_dominio(dominio: str) -> dict[str, Any] | None:
    """Devuelve el dominio por clave exacta o None."""
    return DOMINIOS.get(dominio)


def buscar_por_keywords(texto: str) -> list[tuple[str, dict[str, Any], float]]:
    """Busca dominios cuyas keywords coincidan con el texto.

    Devuelve lista de (clave_dominio, dominio, score) ordenada por relevancia.
    """
    texto_lower = texto.lower()
    resultados = []
    for clave, dominio in DOMINIOS.items():
        score = 0.0
        for kw in dominio["keywords"]:
            if kw.lower() in texto_lower:
                score += 1.0
        if any(w in dominio["nombre"].lower() for w in texto_lower.split()):
            score += 0.5
        if score > 0:
            resultados.append((clave, dominio, score))
    resultados.sort(key=lambda x: x[2], reverse=True)
    return resultados


def keywords_para_dominio(dominio: str, subtema: str | None = None) -> list[str]:
    """Devuelve keywords de busqueda para un dominio (y opcionalmente subtema)."""
    dom = DOMINIOS.get(dominio)
    if dom is None:
        return []
    kws = list(dom["keywords"])
    if subtema and subtema in dom.get("subtemas", {}):
        kws.insert(0, dom["subtemas"][subtema])
    return kws
