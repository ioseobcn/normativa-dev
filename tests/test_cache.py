"""Tests for normativa.cache — SQLite cache with TTL."""

from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone

from normativa.cache import Cache, _SCHEMAS


# ---------------------------------------------------------------------------
# Cache creation and basic operations
# ---------------------------------------------------------------------------


class TestCacheCreation:
    """Test that Cache creates DB file and tables."""

    async def test_creates_db_file(self, tmp_path):
        db_path = tmp_path / "normativa" / "test.db"
        async with Cache(path=db_path) as cache:
            assert db_path.exists()

    async def test_creates_all_tables(self, tmp_path):
        db_path = tmp_path / "test.db"
        async with Cache(path=db_path) as cache:
            stats = await cache.stats()
            for table in _SCHEMAS:
                assert table in stats["tables"]
                assert stats["tables"][table] == 0

    async def test_stats_reports_size(self, tmp_path):
        db_path = tmp_path / "test.db"
        async with Cache(path=db_path) as cache:
            stats = await cache.stats()
            assert stats["size_bytes"] > 0
            assert stats["total_entries"] == 0
            assert stats["path"] == str(db_path)


# ---------------------------------------------------------------------------
# get_or_fetch — store and retrieve
# ---------------------------------------------------------------------------


class TestGetOrFetch:
    """Test get_or_fetch stores and retrieves data."""

    async def test_stores_and_retrieves(self, tmp_path):
        db_path = tmp_path / "test.db"
        async with Cache(path=db_path) as cache:
            fetch_called = 0

            async def fetch():
                nonlocal fetch_called
                fetch_called += 1
                return {"titulo": "Ley de Prueba", "id": "BOE-TEST-001"}

            # First call: should fetch
            result = await cache.get_or_fetch("metadatos", "BOE-TEST-001", fetch)
            assert result == {"titulo": "Ley de Prueba", "id": "BOE-TEST-001"}
            assert fetch_called == 1

            # Second call: should use cache
            result2 = await cache.get_or_fetch("metadatos", "BOE-TEST-001", fetch)
            assert result2 == result
            assert fetch_called == 1  # fetch_fn NOT called again

    async def test_different_keys_fetch_independently(self, tmp_path):
        db_path = tmp_path / "test.db"
        async with Cache(path=db_path) as cache:

            async def fetch_a():
                return {"id": "A"}

            async def fetch_b():
                return {"id": "B"}

            result_a = await cache.get_or_fetch("metadatos", "KEY-A", fetch_a)
            result_b = await cache.get_or_fetch("metadatos", "KEY-B", fetch_b)
            assert result_a["id"] == "A"
            assert result_b["id"] == "B"

    async def test_composite_key_table(self, tmp_path):
        db_path = tmp_path / "test.db"
        async with Cache(path=db_path) as cache:

            async def fetch():
                return {"content": "articulo 29 texto"}

            result = await cache.get_or_fetch(
                "bloques", ("BOE-A-2014-12328", "a29"), fetch
            )
            assert result["content"] == "articulo 29 texto"

            # Retrieve same composite key
            result2 = await cache.get_or_fetch(
                "bloques", ("BOE-A-2014-12328", "a29"), fetch
            )
            assert result2 == result

    async def test_unknown_table_raises(self, tmp_path):
        db_path = tmp_path / "test.db"
        async with Cache(path=db_path) as cache:
            with __import__("pytest").raises(ValueError, match="Unknown table"):
                await cache.get_or_fetch(
                    "nonexistent_table", "key", lambda: None
                )


# ---------------------------------------------------------------------------
# TTL expiration
# ---------------------------------------------------------------------------


class TestTTLExpiration:
    """Test that entries expire based on TTL."""

    async def test_expired_entry_refetches(self, tmp_path):
        db_path = tmp_path / "test.db"
        async with Cache(path=db_path) as cache:
            fetch_count = 0

            async def fetch():
                nonlocal fetch_count
                fetch_count += 1
                return {"version": fetch_count}

            # Store with ttl_hours=0 should never expire
            result = await cache.get_or_fetch(
                "metadatos", "KEY-PERSIST", fetch, ttl_hours=0
            )
            assert result["version"] == 1
            assert fetch_count == 1

            # Should still be cached (never expires)
            result2 = await cache.get_or_fetch(
                "metadatos", "KEY-PERSIST", fetch, ttl_hours=0
            )
            assert result2["version"] == 1
            assert fetch_count == 1

    async def test_force_expire_by_manipulating_db(self, tmp_path):
        """Manually set expires_at in the past, verify re-fetch."""
        db_path = tmp_path / "test.db"
        async with Cache(path=db_path) as cache:
            fetch_count = 0

            async def fetch():
                nonlocal fetch_count
                fetch_count += 1
                return {"v": fetch_count}

            # First fetch
            await cache.get_or_fetch("metadatos", "KEY-EXPIRE", fetch, ttl_hours=1)
            assert fetch_count == 1

            # Manually expire the entry
            past = (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat()
            await cache.db.execute(
                "UPDATE metadatos SET expires_at = ? WHERE key = ?",
                [past, "KEY-EXPIRE"],
            )
            await cache.db.commit()

            # Should re-fetch because entry is expired
            result = await cache.get_or_fetch(
                "metadatos", "KEY-EXPIRE", fetch, ttl_hours=1
            )
            assert fetch_count == 2
            assert result["v"] == 2


# ---------------------------------------------------------------------------
# invalidate
# ---------------------------------------------------------------------------


class TestInvalidate:
    """Test cache invalidation."""

    async def test_invalidate_specific_key(self, tmp_path):
        db_path = tmp_path / "test.db"
        async with Cache(path=db_path) as cache:

            async def fetch():
                return {"data": "test"}

            await cache.get_or_fetch("metadatos", "KEY-1", fetch)
            await cache.get_or_fetch("metadatos", "KEY-2", fetch)

            deleted = await cache.invalidate("metadatos", "KEY-1")
            assert deleted == 1

            stats = await cache.stats()
            assert stats["tables"]["metadatos"] == 1

    async def test_invalidate_all_entries(self, tmp_path):
        db_path = tmp_path / "test.db"
        async with Cache(path=db_path) as cache:

            async def fetch():
                return {"data": "test"}

            await cache.get_or_fetch("metadatos", "KEY-1", fetch)
            await cache.get_or_fetch("metadatos", "KEY-2", fetch)
            await cache.get_or_fetch("metadatos", "KEY-3", fetch)

            deleted = await cache.invalidate("metadatos")
            assert deleted == 3

            stats = await cache.stats()
            assert stats["tables"]["metadatos"] == 0

    async def test_invalidate_unknown_table_raises(self, tmp_path):
        db_path = tmp_path / "test.db"
        async with Cache(path=db_path) as cache:
            with __import__("pytest").raises(ValueError, match="Unknown table"):
                await cache.invalidate("nonexistent")

    async def test_invalidate_nonexistent_key_returns_zero(self, tmp_path):
        db_path = tmp_path / "test.db"
        async with Cache(path=db_path) as cache:
            deleted = await cache.invalidate("metadatos", "DOES-NOT-EXIST")
            assert deleted == 0

    async def test_after_invalidate_refetches(self, tmp_path):
        db_path = tmp_path / "test.db"
        async with Cache(path=db_path) as cache:
            call_count = 0

            async def fetch():
                nonlocal call_count
                call_count += 1
                return {"v": call_count}

            await cache.get_or_fetch("metadatos", "KEY-INV", fetch)
            assert call_count == 1

            await cache.invalidate("metadatos", "KEY-INV")

            result = await cache.get_or_fetch("metadatos", "KEY-INV", fetch)
            assert call_count == 2
            assert result["v"] == 2
