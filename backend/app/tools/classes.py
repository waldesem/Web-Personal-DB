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
    poligraf = "ПФО"
    cancel = "Отменено"
    finish = "Окончено"


class Conclusions(Enum):
    agreed = "СОГЛАСОВАНО"
    comments = "СОГЛАСОВАНО С КОММЕНТАРИЕМ"
    denied = "ОТКАЗАНО В СОГЛАСОВАНИИ"
    canceled = "СНЯТ С ПРОВЕРКИ"


class Relations(Enum):
    similar = "Одно лицо"
    parent_child = "Родители-Дети"
    brother_sister = "Братья-Сестры"
    husband_wife = "Супруг-Супруга"
    relatives = "Родственники"
    others = "Близкая связь"
