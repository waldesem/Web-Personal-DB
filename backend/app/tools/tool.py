from datetime import datetime
import os

from config import Config
from ..depends.depend import current_user


class Folders:
    """Create folder structure for person

    Args:
        region (str): region
        person_id (str): person id
        surname (str): surname
        firstname (str): firstname
        patronymic (str): patronymic

    Attributes:
        url (str): path to main folder

    """

    def __init__(self, region, person_id, surname, firstname, patronymic):
        self.url = os.path.join(
            Config.BASE_PATH,
            region,
            surname[0].upper(),
            f"{person_id}-{surname.upper()} "
            f"{firstname.upper()} "
            f"{patronymic.upper()}".rstrip(),
        )

    @staticmethod
    def _check_url(url):
        """Check if folder exists and create it if not

        Args:
            url (str): folder path

        Returns:
            str: folder path
        """
        if not os.path.isdir(url):
            os.mkdir(url)
        return url

    def create_main_folder(self):
        """Create main folder for person

        Returns:
            str: path to main folder
        """
        return self._check_url(self.url)

    def create_parent_folder(self, folder_name):
        """Create parent folder for person

        Args:
            folder_name (str): parent folder name

        Returns:
            str: path to parent folder
        """
        parent_folder = os.path.join(self.create_main_folder(), folder_name)
        return self._check_url(parent_folder)

    def create_subfolder(self, parent_folder):
        """Create subfolder for person

        Args:
            parent_folder (str): parent folder name

        Returns:
            str: path to subfolder
        """
        subfolder = os.path.join(
            self.url,
            self.create_parent_folder(parent_folder),
            datetime.now().strftime("%Y-%m-%d"),
        )
        return self._check_url(subfolder)


def parse_json(json_dict: dict) -> dict:
    """
    Parses a JSON dictionary and returns a dictionary with the parsed data.

    Args:
        json_dict (dict): The JSON dictionary to parse.

    Returns:
        dict: The parsed dictionary containing the resume, addresses, contacts, documents, staffs, previous, educations, and workplaces.
    """
    json_data = {
        "resume": {
            "region": current_user["region"],
            "firstname": json_dict.get("firstName"),
            "surname": json_dict.get("lastName"),
            "patronymic": json_dict.get("midName"),
            "birthday": datetime.strptime(json_dict["birthday"], "%Y-%m-%d").date()
            if json_dict.get("birthday")
            else None,
            "birthplace": json_dict.get("birthplace"),
            "citizenship": json_dict.get("citizen"),
            "dual": json_dict.get("additionalCitizenship"),
            "inn": json_dict.get("inn"),
            "snils": json_dict.get("snils"),
            "marital": json_dict.get("maritalStatus"),
        },
        "addresses": [
            {
                "view": "Адрес проживания",
                "addresses": json_dict.get("validAddress"),
            },
            {
                "view": "Адрес регистрации",
                "addresses": json_dict.get("regAddress"),
            },
        ],
        "contacts": [
            {"view": "Телефон", "contact": json_dict.get("contactPhone")},
            {"view": "Электронная почта", "contact": json_dict.get("email")},
        ],
        "documents": [
            {
                "view": "Паспорт гражданина России",
                "number": json_dict.get("passportNumber"),
                "digits": json_dict.get("passportSerial"),
                "issue": datetime.strptime(
                    json_dict["passportIssueDate"], "%Y-%m-%d"
                ).date()
                if json_dict.get("passportIssueDate")
                else None,
                "agency": json_dict.get("passportIssuedBy"),
            }
        ],
        "staffs": [
            {
                "position": json_dict.get("positionName"),
                "department": json_dict.get("department"),
            }
        ],
        "previous": [],
        "educations": [],
        "workplaces": [],
        "affilations": [],
    }
    for item, values in json_dict.items():
        if values:
            views = {
                "publicOfficeOrganizations": "Являлся государственным или муниципальным служащим",
                "stateOrganizations": "Являлся государственным должностным лицом",
                "relatedPersonsOrganizations": "Связанные лица работают в госудраственных организациях",
                "organizations": "Участвует в деятельности коммерческих организаций",
            }
            if item in views.keys():
                for org in values:
                    json_data["affilations"].append({
                        "view": views[item],
                        "organization": org.get("organization"),
                        "position": org.get("position"),
                        "inn": org.get("inn")
                    })

            elif item == "previous":
                for prev in values:
                    json_data["previous"].append({
                        "firstname": prev.get("firstNameBeforeChange"),
                        "surname": prev.get("lastNameBeforeChange"),
                        "patronymic": prev.get("midNameBeforeChange"),
                        "changed": prev.get("yearOfChange"),
                        "reason": prev.get("reason")
                    })
                    
            elif item == "education":
                for edu in values:
                    json_data["educations"].append({
                        "view": edu.get("educationType"),
                        "institution": edu.get("institutionName"),
                        "finished": edu.get("endYear"),
                        "speciality": edu.get("specialty")
                    })
                    
            elif item == "experience":
                for exp in values:
                    json_data["workplaces"].append({
                        "starts": datetime.strptime(
                                    exp["beginDate"], "%Y-%m-%d"
                                ).date() if exp.get("beginDate") else None,
                        "finished": datetime.strptime(
                                    exp["endDate"], "%Y-%m-%d"
                                ).date() if exp.get("endDate") else None,
                        "now_work":  True if exp.get("currentJob") else False 
                        "workplace": exp.get("name"),
                        "addresses": exp.get("address"),
                        "position": exp.get("position")
                        "reason": exp.get("fireReason")
                    })
    return (
        json_data
        if json_data["resume"]["surname"]
        and json_data["resume"]["firstname"]
        and json_data["resume"]["birthday"]
        else None
    )