from enum import Enum


class Regions(Enum):
    main = "Главный офис"
    south = "Региональный центр Юг"
    west = "Региональный центр Запад"
    ural = "Региональный центр Урал"
    east = "Региональный центр Восток"


class Statuses(Enum):
    manual = "Правка"
    poligraf = "ПФО"
    finish = "Окончен"
    saved = "Сохранен"


class Conclusions(Enum):
    saved = "СОХРАНЕНО"
    agreed = "СОГЛАСОВАНО"
    comments = "СОГЛАСОВАНО С КОММЕНТАРИЕМ"
    denied = "ОТКАЗАНО В СОГЛАСОВАНИИ"


class Relations(Enum):
    similar = "Одно лицо"
    parent_child = "Родители-Дети"
    brother_sister = "Братья-Сестры"
    husband_wife = "Супруг-Супруга"
    relatives = "Родственники"
    others = "Близкая связь"


class Educations(Enum):
    primary = "Основное общее"
    secondary = "Среднее общее"
    special = "Среднее профессиональное"
    higher = "Высшее"
    unfinished = "Неоконченное высшее образование"
    others = "Другое образование"


class Documents(Enum):
    passport = "Паспорт гражданина России"
    foreign_passport = "Загранпаспорт"
    others = "Другое"


class Addresses(Enum):
    registration = "Адрес регистрации"
    actual = "Адрес проживания"
    others = "Другое"


class Contacts(Enum):
    phone = "Телефон"
    email = "Электронная почта"
    others = "Другое"


class Affiliates(Enum):
    state = "Являлся государственным/муниципальным служащим"
    public = "Являлся государственным должностным лицом"
    related = "Связанные лица работают в государственных организациях"
    commercial = "Участвует в деятельности коммерческих организаций"


class Poligrafs(Enum):
    check = 'Проверка кандидата'
    verification = 'Служебная проверка'
    investigation = 'Служебное расследование'
    planned = 'Плановое мероприятие'