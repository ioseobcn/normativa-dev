"""Shared singletons for BOEClient and Cache, lazy-initialized."""

from __future__ import annotations

from normativa.boe_client import BOEClient
from normativa.cache import Cache

_client: BOEClient | None = None
_cache: Cache | None = None


async def get_client() -> BOEClient:
    """Return a shared BOEClient, opening it on first call."""
    global _client
    if _client is None:
        _client = BOEClient()
        await _client.__aenter__()
    return _client


async def get_cache() -> Cache:
    """Return a shared Cache, opening it on first call."""
    global _cache
    if _cache is None:
        _cache = Cache()
        await _cache.__aenter__()
    return _cache
