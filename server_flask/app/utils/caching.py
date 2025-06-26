"""Caching module."""

from __future__ import annotations


class DictCache[T]:
    """Dict Cache."""

    def __init__(self, max_size: int | None = None) -> None:
        """Init cache."""
        self.max_size = max_size
        self._data = {}

    def get(self, key: str) -> T | None:
        """Get cache key."""
        return self._data.get(key)

    def set(self, key: str, value: T) -> None:
        """Set cache value."""
        self._data[key] = value
        if self.max_size and len(self._data) > self.max_size:
            key = next(iter(self._data))
            self.delete(key)

    def delete(self, key: str) -> None:
        """Delete cache key."""
        if self._data.get(key):
            del self._data[key]

    def clear(self) -> None:
        """Clear cache."""
        self._data.clear()
