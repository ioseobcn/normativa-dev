"""Domain registry — loads and searches domain configurations."""

from __future__ import annotations

import importlib
from typing import Any

from normativa.domains import AVAILABLE_DOMAINS
from normativa.domains._base import DomainConfig


_cache: dict[str, DomainConfig] = {}


def load_domain(name: str) -> DomainConfig:
    """Import and return DomainConfig from domains/{name}.py.

    The module must expose a top-level ``DOMAIN`` variable of type DomainConfig.
    """
    if name in _cache:
        return _cache[name]

    if name not in AVAILABLE_DOMAINS:
        raise ValueError(
            f"Unknown domain '{name}'. Available: {AVAILABLE_DOMAINS}"
        )

    module = importlib.import_module(f"normativa.domains.{name}")
    config: DomainConfig = getattr(module, "DOMAIN", None)
    if config is None or not isinstance(config, DomainConfig):
        raise AttributeError(
            f"Module 'normativa.domains.{name}' must expose a DOMAIN: DomainConfig"
        )

    _cache[name] = config
    return config


def list_domains() -> list[dict[str, Any]]:
    """Return summary info for every available domain."""
    result: list[dict[str, Any]] = []
    for name in AVAILABLE_DOMAINS:
        try:
            cfg = load_domain(name)
            result.append({
                "slug": cfg.slug,
                "nombre": cfg.nombre,
                "descripcion": cfg.descripcion,
                "num_leyes": len(cfg.leyes_clave),
            })
        except Exception:
            result.append({
                "slug": name,
                "nombre": name,
                "descripcion": "(error loading domain)",
                "num_leyes": 0,
            })
    return result


def search_domains(query: str) -> list[dict[str, Any]]:
    """Search across all domains by terms, use cases, subtema names, or law names.

    The query is split into individual words so that "RGPD cookies" matches
    both proteccion_datos (RGPD) and digital (cookies), returning results
    from multiple domains sorted by relevance score.

    Returns a list of matching entries with domain slug, match type, and details.
    """
    words = [w.lower() for w in query.split() if w]
    if not words:
        return []

    results: list[dict[str, Any]] = []

    for name in AVAILABLE_DOMAINS:
        try:
            cfg = load_domain(name)
        except Exception:
            continue

        score = 0
        match_reasons: list[str] = []

        for word in words:
            # Search in domain-level terms
            if word in cfg.nombre.lower() or word in cfg.descripcion.lower():
                score += 10
                match_reasons.append(f"nombre/descripcion: {word}")

            for term in cfg.terminos_busqueda:
                if word in term.lower():
                    score += 5
                    match_reasons.append(f"termino: {term}")

            # Search in use cases
            for caso_slug, caso_desc in cfg.casos_uso.items():
                if word in caso_slug.lower() or word in caso_desc.lower():
                    score += 8
                    match_reasons.append(f"caso_uso: {caso_slug}")

            # Search in subtemas
            for sub in cfg.subtemas:
                if word in sub.nombre.lower() or word in sub.descripcion.lower():
                    score += 7
                    match_reasons.append(f"subtema: {sub.slug}")
                for term in sub.terminos_busqueda:
                    if word in term.lower():
                        score += 4
                        match_reasons.append(f"subtema_termino: {term}")
                for caso in sub.casos_uso:
                    if word in caso.lower():
                        score += 6
                        match_reasons.append(f"subtema_caso: {caso}")

            # Search in law names
            for boe_id, ley in cfg.leyes_clave.items():
                if word in ley.nombre_corto.lower() or word in ley.titulo_oficial.lower():
                    score += 9
                    match_reasons.append(f"ley: {ley.nombre_corto}")

        if score > 0:
            results.append({
                "slug": cfg.slug,
                "nombre": cfg.nombre,
                "score": score,
                "matches": match_reasons[:5],  # Top 5 reasons
            })

    results.sort(key=lambda r: r["score"], reverse=True)
    return results
