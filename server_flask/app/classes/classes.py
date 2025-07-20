"""Enums and classes module."""

from enum import Enum


class Roles(Enum):
    """Enum class for user roles."""

    admin = "admin"
    api = "api"
    user = "user"
    guest = "guest"


class Conclusions(Enum):
    """Enum class for conclusions."""

    agreed = "СОГЛАСОВАНО"
    comments = "СОГЛАСОВАНО С КОММЕНТАРИЕМ"
    denied = "ОТКАЗАНО В СОГЛАСОВАНИИ"
    cancel = "СНЯТ С ПРОВЕРКИ"


class Decisions(Enum):
    """Enum class for decisions."""

    agreed = "БЕЗ ЗАМЕЧАНИЙ"
    comments = "С КОММЕНТАРИЯМИ"
    cancel = "ОТКАЗ ОТ ПРОВЕРКИ"
    denied = "НЕГАТИВ"
