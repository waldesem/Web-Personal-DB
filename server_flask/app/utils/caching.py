"""Caching module."""

from __future__ import annotations


class DictCache[T]:
    """Dict Cache."""

    def __init__(self, max_size: int = None) -> None:
        """Init cache."""
        self.max_size = max_size
        self.data = {}

    def get(self, key: str) -> T | None:
        """Get cache key."""
        return self.data.get(key)

    def set(self, key: str, value: T) -> None:
        """Set cache value."""
        self.data[key] = value
        if max_size and len(self.data) > max_size:
            del next(iter(self.data))

    def delete(self, key: str) -> None:
        """Delete cache key."""
        if self.data.get(key):
            del self.data[key]

    def clear(self) -> None:
        """Clear cache."""
        self.data.clear()
