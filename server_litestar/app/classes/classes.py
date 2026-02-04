"""Enums and classes module."""

from enum import StrEnum


class Roles(StrEnum):
    """Users roles."""

    admin = "admin"
    api = "api"
    user = "user"
    guest = "guest"


class Conclusions(StrEnum):
    """Checks conclusions."""

    agreed = "СОГЛАСОВАНО"
    comments = "СОГЛАСОВАНО С КОММЕНТАРИЕМ"
    denied = "ОТКАЗАНО В СОГЛАСОВАНИИ"
    cancel = "СНЯТ С ПРОВЕРКИ"


class Decisions(StrEnum):
    """Poligrafs decisions."""

    agreed = "БЕЗ ЗАМЕЧАНИЙ"
    comments = "С КОММЕНТАРИЯМИ"
    cancel = "ОТКАЗ ОТ ПРОВЕРКИ"
    denied = "НЕГАТИВ"


class ItemCategory(StrEnum):
    """Item categories."""

    ADDRESSES = "addresses"
    AFFILATIONS = "affilations"
    CHECKS = "checks"
    CONTACTS = "contacts"
    DOCUMENTS = "documents"
    EDUCATIONS = "educations"
    INQUIRIES = "inquiries"
    INVESTIGATIONS = "investigations"
    PREVIOUS = "previous"
    POLIGRAFS = "poligrafs"
    STAFFS = "staffs"
    WORKPLACES = "workplaces"
