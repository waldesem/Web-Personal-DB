from enum import Enum


class Regions(Enum):

    MAIN_OFFICE = "Главный офис"
    SOUTH_REGION = "Региональный центр Юг"
    WEST_REGION = "Региональный центр Запад"
    URAL_REGION = "Региональный центр Урал"
    EAST_REGION = "Региональный центр Восток"


class Roles(Enum):

    admin = "admin"
    user = "user"
    api = "api"


class Statuses(Enum):

    new = "Новый"
    repeat = "Повторный"
    update = "Обновлен"
    manual = "Проверка"
    save = "Сохранен"
    robot = "Робот"
    reply = "Обработан"
    poligraf = "ПФО"
    cancel = "Отменено"
    error = "Ошибка"
    finish = "Окончено"

class Conclusions(Enum):

    agreed = "СОГЛАСОВАНО"
    with_comment = "СОГЛАСОВАНО С КОММЕНТАРИЕМ"
    denied = "ОТКАЗАНО В СОГЛАСОВАНИИ"
    saved = "СОХРАНЕН"
    canceled = "ОТМЕНЕНО"
