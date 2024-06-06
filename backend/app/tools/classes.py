from enum import Enum


class Regions(Enum):
    main = "Главный офис"
    south = "Региональный центр Юг"
    west = "Региональный центр Запад"
    ural = "Региональный центр Урал"
    east = "Региональный центр Восток"


class Statuses(Enum):
    new = "Новый"
    repeat = "Повторный"
    update = "Обновлен"
    manual = "Проверка"
    save = "Сохранен"
    robot = "Робот"
    poligraf = "ПФО"
    error = "Ошибка"
    cancel = "Отменено"
    finish = "Окончено"


class Conclusions(Enum):
    agreed = "СОГЛАСОВАНО"
    comments = "СОГЛАСОВАНО С КОММЕНТАРИЕМ"
    denied = "ОТКАЗАНО В СОГЛАСОВАНИИ"
    saved = "СОХРАНЕН"
    canceled = "СНЯТ С ПРОВЕРКИ"
