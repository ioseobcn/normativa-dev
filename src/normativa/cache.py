"""Lightweight SQLite cache for normativa using aiosqlite."""

from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Awaitable

import aiosqlite

DEFAULT_PATH = Path.home() / ".cache" / "normativa" / "cache.db"

# TTL defaults in hours (0 = never expires)
TTL_DEFAULTS: dict[str, int] = {
    "metadatos": 168,
    "analisis": 168,
    "indices": 72,
    "bloques": 72,
    "sumarios": 0,
    "auxiliares": 720,
}

# Table schemas: table_name -> (key_columns, has_composite_pk)
_SCHEMAS: dict[str, tuple[list[str], bool]] = {
    "metadatos": (["key"], False),
    "analisis": (["key"], False),
    "indices": (["key"], False),
    "bloques": (["boe_id", "bloque_id"], True),
    "sumarios": (["tipo", "fecha"], True),
    "auxiliares": (["key"], False),
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _expires(ttl_hours: int) -> str | None:
    if ttl_hours <= 0:
        return None
    return (datetime.now(timezone.utc) + timedelta(hours=ttl_hours)).isoformat()


class Cache:
    """Async SQLite cache with per-table TTL and composite key support."""

    def __init__(self, path: str | Path | None = None) -> None:
        self.path = Path(path) if path else DEFAULT_PATH
        self._db: aiosqlite.Connection | None = None

    async def __aenter__(self) -> "Cache":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._db = await aiosqlite.connect(str(self.path))
        self._db.row_factory = aiosqlite.Row
        await self._db.execute("PRAGMA journal_mode=WAL")
        await self._create_tables()
        return self

    async def __aexit__(self, *exc: Any) -> None:
        if self._db:
            await self._db.close()
            self._db = None

    @property
    def db(self) -> aiosqlite.Connection:
        if self._db is None:
            raise RuntimeError("Cache not opened. Use 'async with Cache() as c:'")
        return self._db

    async def _create_tables(self) -> None:
        for table, (key_cols, composite) in _SCHEMAS.items():
            cols_def = ", ".join(f"{c} TEXT NOT NULL" for c in key_cols)
            pk_def = ", ".join(key_cols)
            ddl = (
                f"CREATE TABLE IF NOT EXISTS {table} ("
                f"  {cols_def},"
                f"  data TEXT NOT NULL,"
                f"  fetched_at TEXT NOT NULL,"
                f"  expires_at TEXT,"
                f"  PRIMARY KEY ({pk_def})"
                f")"
            )
            await self.db.execute(ddl)
        await self.db.commit()

    def _key_where(self, table: str, key: Any) -> tuple[str, list[str]]:
        """Build WHERE clause and params for a given key.

        For single-key tables, key is a string.
        For composite-key tables, key is a tuple.
        """
        key_cols = _SCHEMAS[table][0]
        if len(key_cols) == 1:
            return f"{key_cols[0]} = ?", [str(key)]
        if not isinstance(key, (tuple, list)) or len(key) != len(key_cols):
            raise ValueError(
                f"Table '{table}' expects composite key {key_cols}, got {key!r}"
            )
        where = " AND ".join(f"{c} = ?" for c in key_cols)
        return where, [str(k) for k in key]

    async def get_or_fetch(
        self,
        table: str,
        key: Any,
        fetch_fn: Callable[[], Awaitable[Any]],
        ttl_hours: int | None = None,
    ) -> Any:
        """Return cached data or call fetch_fn, store result, and return it."""
        if table not in _SCHEMAS:
            raise ValueError(f"Unknown table: {table}")

        if ttl_hours is None:
            ttl_hours = TTL_DEFAULTS.get(table, 72)

        where, params = self._key_where(table, key)

        row = await self.db.execute_fetchall(
            f"SELECT data, expires_at FROM {table} WHERE {where}", params
        )

        if row:
            r = row[0]
            expires = r["expires_at"] if isinstance(r, aiosqlite.Row) else r[1]
            data_str = r["data"] if isinstance(r, aiosqlite.Row) else r[0]
            if expires is None or expires > _now():
                return json.loads(data_str)

        # Cache miss or expired: fetch fresh data
        result = await fetch_fn()
        data_json = json.dumps(result, ensure_ascii=False, default=str)
        now = _now()
        exp = _expires(ttl_hours)

        key_cols = _SCHEMAS[table][0]
        _, key_params = self._key_where(table, key)
        placeholders = ", ".join("?" for _ in key_cols)
        col_names = ", ".join(key_cols)

        await self.db.execute(
            f"INSERT OR REPLACE INTO {table} ({col_names}, data, fetched_at, expires_at) "
            f"VALUES ({placeholders}, ?, ?, ?)",
            [*key_params, data_json, now, exp],
        )
        await self.db.commit()
        return result

    async def invalidate(self, table: str, key: Any | None = None) -> int:
        """Clear specific entry or all entries in a table. Returns rows deleted."""
        if table not in _SCHEMAS:
            raise ValueError(f"Unknown table: {table}")

        if key is None:
            cursor = await self.db.execute(f"DELETE FROM {table}")
        else:
            where, params = self._key_where(table, key)
            cursor = await self.db.execute(
                f"DELETE FROM {table} WHERE {where}", params
            )
        await self.db.commit()
        return cursor.rowcount

    async def stats(self) -> dict[str, Any]:
        """Return cache size on disk and entry counts per table."""
        counts: dict[str, int] = {}
        for table in _SCHEMAS:
            rows = await self.db.execute_fetchall(
                f"SELECT COUNT(*) as cnt FROM {table}"
            )
            counts[table] = rows[0][0] if rows else 0

        total_entries = sum(counts.values())
        size_bytes = self.path.stat().st_size if self.path.exists() else 0

        return {
            "path": str(self.path),
            "size_bytes": size_bytes,
            "size_mb": round(size_bytes / (1024 * 1024), 2),
            "total_entries": total_entries,
            "tables": counts,
        }
