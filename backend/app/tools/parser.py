import os
from datetime import datetime

from config import Config

from ..classes.classes import Relations, Statuses
from ..databases.database import execute, select_single
from ..depends.depend import current_user
from ..models.models import Person
from .jsoned import parse_json


class Folders:

    def __init__(self, region, person_id, surname, firstname, patronymic):
        self.url = os.path.join(
            region,
            Config.BASE_PATH,
            surname[0].upper(),
            f"{person_id}-{surname.upper()} "
            f"{firstname.upper()} "
            f"{patronymic.upper()}".rstrip(),
        )

    @staticmethod
    def _check_url(url):
        if not os.path.isdir(url):
            os.mkdir(url)
        return url

    def create_main_folder(self):
        return self._check_url(self.url)

    def create_parent_folder(self, folder_name):
        parent_folder = os.path.join(self.create_main_folder(), folder_name)
        return self._check_url(parent_folder)

    def create_subfolder(self, parent_folder):
        subfolder = os.path.join(
            self.url,
            self.create_parent_folder(parent_folder),
            datetime.now().strftime("%Y-%m-%d"),
        )
        return self._check_url(subfolder)


class Resume:
    def __init__(self, resume: dict):
        self.resume = Person(**resume).dict()
        self.resume['user_id'] = current_user['id']

    @staticmethod
    def get_person(surname, firstname, patronymic, birthday):
        stmt = """
        SELECT * FROM persons
        WHERE surname LIKE upper('%{}%')
        AND firstname LIKE upper('%{}%')
        AND patronymic LIKE upper('%{}%')
        AND birthday = ?
        """.format(surname, firstname, patronymic)
        return select_single(stmt, (birthday,))

    def update_status(self):
        try:
            self.resume['status'] = Statuses.manual.value
            self.resume['user_id'] = current_user["id"]
            keys, args = zip(*self.resume.items())
            stmt = "INSERT OR REPLACE INTO persons ({}) VALUES ({})".format(
                ", ".join(keys),
                ", ".join(["?" for _ in keys]),
            )
            person_id = execute(stmt, args)
            folders = Folders(
                current_user["region"],
                person_id,
                self.resume["surname"],
                self.resume["firstname"],
                self.resume.get("patronymic", ""),
            )
            path = folders.create_main_folder()
            execute(
                "UPDATE persons SET path = ? WHERE id = ?",
                (
                    path,
                    person_id,
                ),
            )
            return person_id
        except Exception as e:
            print(e)


class Anketa(Resume):
    def __init__(self, json_data):
        self.anketa = parse_json(json_data)
        super().__init__(self.anketa["resume"])
        self.person_id = self.update_status()

    def parse_anketa(self):
        if len(self.anketa["previous"]):
            self.parse_relations()
        self.save_items()
        return self.person_id

    def parse_relations(self):
        for item in self.anketa["previous"]:
            surname = item.get("surname", self.resume["surname"])
            firstname = item.get("firstname", self.resume["firstname"])
            patronymic = item.get("patronymic", self.resume.get("patronymic", ""))
            birthday = self.resume["birthday"]
            relation = self.get_person(surname, firstname, patronymic, birthday)
            if relation:
                execute(
                    "INSERT INTO relations (relation, person_id, relation_id) VALUES (?, ?, ?)",
                    [
                        (
                            Relations.similar.value,
                            self.person_id,
                            relation.id,
                        ),
                        (
                            Relations.similar.value,
                            relation.id,
                            self.person_id,
                        ),
                    ],
                )

    def save_items(self):
        for table, values in self.anketa.items():
            if table == "resume":
                continue
            for item in values:
                item["person_id"] = self.person_id
                keys, args = zip(*item.items())
                stmt = f"INSERT INTO {table} ({','.join(keys)}) VALUES ({','.join(['?' for _ in keys])})"
                execute(stmt, tuple(args))
