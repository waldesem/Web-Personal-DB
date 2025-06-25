class DictCache:
    """Dict Cache."""

    def __init__(self) -> None:
        """Init cache."""
        self.data = {}

    def get(self, key: str) -> Any | None:
        """Get cache key."""
        return self.data.get(key)

    def set(self, key: str, value: Any) -> None:
        """Set cache value."""
        self.data[key] = value

    def delete(self, key: str) -> None:
        """Delete cache key."""
        if self.data.get(key):
            delete self.data[key]

    def clear(self) -> None:
        """Clear cache."""
        self.data.clear()