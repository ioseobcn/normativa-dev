"""Domain configuration dataclasses for normativa."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class EURef:
    """Reference to an EU legislative act."""

    celex: str  # "32016R0679" (GDPR)
    titulo: str  # "Reglamento General de Proteccion de Datos"
    tipo: str  # "reglamento", "directiva", "decision"
    eli_url: str = ""  # "http://data.europa.eu/eli/reg/2016/679/oj"
    relacion: str = "transpone"  # "transpone", "implementa", "complementa", "deroga"


@dataclass
class LeyRef:
    """Reference to a specific Spanish law in the BOE."""

    boe_id: str  # "BOE-A-2006-20764"
    nombre_corto: str  # "Ley IRPF"
    titulo_oficial: str  # Full official title
    rango: str  # "Ley", "Real Decreto", "Real Decreto Legislativo", etc.
    articulos_clave: dict[str, str] = field(default_factory=dict)
    # {"a35": "Rendimientos del trabajo", "a96": "Obligacion de declarar"}
    eu_refs: list[EURef] = field(default_factory=list)
    # EU legislation this law transposes/implements


@dataclass
class Subtema:
    """A thematic subdivision within a domain."""

    slug: str  # "irpf"
    nombre: str  # "IRPF"
    descripcion: str
    leyes: list[str] = field(default_factory=list)  # BOE IDs
    materias_boe: list[int] = field(default_factory=list)  # Materia codes
    terminos_busqueda: list[str] = field(default_factory=list)
    casos_uso: list[str] = field(default_factory=list)


@dataclass
class DomainConfig:
    """Full configuration for a legal domain."""

    slug: str
    nombre: str
    descripcion: str
    leyes_clave: dict[str, LeyRef] = field(default_factory=dict)  # BOE ID -> LeyRef
    subtemas: list[Subtema] = field(default_factory=list)
    materias_boe: list[int] = field(default_factory=list)
    departamentos_boe: list[str] = field(default_factory=list)
    terminos_busqueda: list[str] = field(default_factory=list)
    dominios_relacionados: list[str] = field(default_factory=list)
    casos_uso: dict[str, str] = field(default_factory=dict)  # slug -> description
