from enum import Enum


class Regions(Enum):

    MAIN_OFFICE = "Главный офис"
    SOUTH_REGION = "Региональный центр Юг"
    WEST_REGION = "Региональный центр Запад"
    URAL_REGION = "Региональный центр Урал"
    EAST_REGION = "Региональный центр Восток"


class Groups(Enum):

    admins = "Admins"
    staffsec = "StaffSec"
    rest = "REST"


class Roles(Enum):

    admin = "admin"
    user = "user"
    api = "API"


class Categories(Enum):

    candidate = "Кандидат"
    staff = "Сотрудник"
    vip = "ВИП"


class Statuses(Enum):

    new = "Новый"
    repeat = "Повторный"
    update = "Обновлен"
    manual = "Проверка"
    save = "Сохранен"
    robot = "Робот"
    reply = "Обработан"
    poligraf = "ПФО"
    finish = "Окончено"
    cancel = "Отменено"
    error = "Ошибка"


class Conclusions(Enum):

    agreed = "СОГЛАСОВАНО"
    with_comment = "СОГЛАСОВАНО С КОММЕНТАРИЕМ"
    denied = "ОТКАЗАНО В СОГЛАСОВАНИИ"
    saved = "СОХРАНЕН"
    canceled = "ОТМЕНЕНО"
