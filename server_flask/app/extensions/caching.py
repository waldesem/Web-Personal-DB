class DictCache:
    """Dict Cache."""

    def __init__(self) -> None:
        """Init cache."""
        self.data = {}

    def get(self, key: str) -> Any | None:
        """Get cache key."""
        return self.data.get(key)

    def set(self, key: str, value: Any) -> None:
        """Delete cache value."""
        self.data[key] = value

    def delete(self, key: str) -> None:
        delete self.data[key]
