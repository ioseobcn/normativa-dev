"""Tests for normativa.registry — domain loading, listing, and search."""

from __future__ import annotations

import pytest

from normativa.registry import list_domains, load_domain, search_domains
from normativa.domains._base import DomainConfig
from normativa.domains import AVAILABLE_DOMAINS


# ---------------------------------------------------------------------------
# list_domains
# ---------------------------------------------------------------------------


class TestListDomains:
    """Test list_domains returns summaries for all registered domains."""

    def test_returns_at_least_7_domains(self):
        domains = list_domains()
        assert len(domains) >= 7

    def test_each_domain_has_required_keys(self):
        domains = list_domains()
        for d in domains:
            assert "slug" in d
            assert "nombre" in d
            assert "descripcion" in d
            assert "num_leyes" in d

    def test_fiscal_is_present(self):
        domains = list_domains()
        slugs = [d["slug"] for d in domains]
        assert "fiscal" in slugs

    def test_all_available_domains_listed(self):
        domains = list_domains()
        slugs = {d["slug"] for d in domains}
        for name in AVAILABLE_DOMAINS:
            assert name in slugs


# ---------------------------------------------------------------------------
# load_domain
# ---------------------------------------------------------------------------


class TestLoadDomain:
    """Test load_domain loads and returns DomainConfig objects."""

    def test_fiscal_returns_domain_config(self):
        cfg = load_domain("fiscal")
        assert isinstance(cfg, DomainConfig)
        assert cfg.slug == "fiscal"

    def test_fiscal_has_4_leyes(self):
        cfg = load_domain("fiscal")
        assert len(cfg.leyes_clave) == 4

    def test_fiscal_leyes_have_boe_ids(self):
        cfg = load_domain("fiscal")
        for boe_id in cfg.leyes_clave:
            assert boe_id.startswith("BOE-")

    def test_fiscal_has_subtemas(self):
        cfg = load_domain("fiscal")
        assert len(cfg.subtemas) >= 4
        slugs = [s.slug for s in cfg.subtemas]
        assert "irpf" in slugs
        assert "iva" in slugs

    def test_laboral_loads(self):
        cfg = load_domain("laboral")
        assert cfg.slug == "laboral"
        assert len(cfg.leyes_clave) >= 1

    def test_proteccion_datos_loads(self):
        cfg = load_domain("proteccion_datos")
        assert cfg.slug == "proteccion_datos"

    def test_nonexistent_domain_raises(self):
        with pytest.raises(ValueError, match="Unknown domain"):
            load_domain("nonexistent_domain_xyz")

    def test_all_available_domains_load(self):
        for name in AVAILABLE_DOMAINS:
            cfg = load_domain(name)
            assert isinstance(cfg, DomainConfig)
            assert cfg.slug == name


# ---------------------------------------------------------------------------
# EU refs presence
# ---------------------------------------------------------------------------


class TestEURefs:
    """Test that EU references are present in relevant domains."""

    def test_fiscal_has_eu_refs(self):
        cfg = load_domain("fiscal")
        eu_ref_count = sum(
            len(ley.eu_refs) for ley in cfg.leyes_clave.values()
        )
        assert eu_ref_count >= 2  # IVA directive + ATAD at minimum

    def test_proteccion_datos_has_rgpd_ref(self):
        cfg = load_domain("proteccion_datos")
        all_eu_refs = []
        for ley in cfg.leyes_clave.values():
            all_eu_refs.extend(ley.eu_refs)
        celex_ids = [r.celex for r in all_eu_refs]
        assert "32016R0679" in celex_ids  # RGPD

    def test_digital_has_eu_refs(self):
        cfg = load_domain("digital")
        eu_ref_count = sum(
            len(ley.eu_refs) for ley in cfg.leyes_clave.values()
        )
        assert eu_ref_count >= 1  # e-Commerce directive at minimum

    def test_eu_ref_fields_populated(self):
        cfg = load_domain("proteccion_datos")
        for ley in cfg.leyes_clave.values():
            for ref in ley.eu_refs:
                assert ref.celex
                assert ref.titulo
                assert ref.tipo in ("reglamento", "directiva", "decision")
                assert ref.relacion in (
                    "transpone", "implementa", "complementa", "deroga"
                )


# ---------------------------------------------------------------------------
# search_domains
# ---------------------------------------------------------------------------


class TestSearchDomains:
    """Test search_domains cross-domain search."""

    def test_rgpd_cookies_returns_two_domains(self):
        results = search_domains("RGPD cookies")
        slugs = [r["slug"] for r in results]
        assert "proteccion_datos" in slugs
        assert "digital" in slugs

    def test_results_sorted_by_score(self):
        results = search_domains("IRPF impuesto renta")
        if len(results) >= 2:
            assert results[0]["score"] >= results[1]["score"]

    def test_empty_query_returns_empty(self):
        results = search_domains("")
        assert results == []

    def test_single_term_search(self):
        results = search_domains("IVA")
        assert len(results) >= 1
        slugs = [r["slug"] for r in results]
        assert "fiscal" in slugs

    def test_results_have_required_keys(self):
        results = search_domains("laboral")
        for r in results:
            assert "slug" in r
            assert "nombre" in r
            assert "score" in r
            assert "matches" in r

    def test_no_match_returns_empty(self):
        results = search_domains("xyznonexistent123")
        assert results == []
