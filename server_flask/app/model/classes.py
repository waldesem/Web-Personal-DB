from enum import Enum


class Roles(Enum):
    admin = "admin"
    user = "user"
    guest = "guest"
    

class Regions(Enum):
    main = "Главный офис"
    south = "РЦ Юг"
    west = "РЦ Запад"
    ural = "РЦ Урал"
    east = "РЦ Восток"


class Conclusions(Enum):
    agreed = "СОГЛАСОВАНО"
    comments = "СОГЛАСОВАНО С КОММЕНТАРИЕМ"
    denied = "ОТКАЗАНО В СОГЛАСОВАНИИ"
