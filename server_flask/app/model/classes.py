"""Module contains classes used in the application."""

from enum import Enum


class Roles(Enum):
    """Enum class for user roles."""

    admin = "admin"
    user = "user"
    guest = "guest"


class Regions(Enum):
    """Enum class for regions."""

    main = "Главный офис"
    south = "РЦ Юг"
    west = "РЦ Запад"
    ural = "РЦ Урал"
    east = "РЦ Восток"


class Conclusions(Enum):
    """Enum class for conclusions."""

    agreed = "СОГЛАСОВАНО"
    comments = "СОГЛАСОВАНО С КОММЕНТАРИЕМ"
    denied = "ОТКАЗАНО В СОГЛАСОВАНИИ"
    cancel = "СНЯТ С ПРОВЕРКИ"


class Decisions(Enum):
    """Enum class for decisions."""

    agreed = "БЕЗ ЗАМЕЧАНИЙ"
    comments = "С КОММЕНТАРИЯМИ"
    denied = "НЕГАТИВ"