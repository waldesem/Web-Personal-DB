"""Caching module."""

from __future__ import annotations

from collections import OrderedDict
from typing import Any


class Cache:
    """A simple cache database.

    data = {
        "1": {
            "persons": "",
            "staffs": [],
            ...,
        },
    }
    """

    def __init__(self) -> None:
        """Initialize the database."""
        self.data: OrderedDict[str, dict[str, Any]] = OrderedDict()

    def get_data(self, person_id: str, item: str) -> str | list:
        """Get the value of a keys."""
        if values := self.data.get(str(person_id)):
            self.data.move_to_end(str(person_id))
            return values.get(item)
        return values

    def set_data(self, person_id: str, item: str, value: str | list) -> None:
        """Set the value of a key."""
        if person_id not in self.data:
            self.clear_data()
            self.data[person_id] = {}
        self.data[person_id][item] = value

    def delete_data(self, person_id: str) -> None:
        """Clear the database."""
        if person_id in self.data:
            del self.data[person_id]

    def clear_data(self) -> None:
        """Check old keys."""
        if len(self.data) > 10:
            self.data.popitem(last=False)
