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
                    organization = {}
                    organization["view"] = views[item]
                    for k, v in org.items():
                        match k:
                            case "organization":
                                organization["name"] = v
                            case "position":
                                organization["position"] = v
                            case "inn":
                                organization["inn"] = v
                    json_data["affilations"].append(organization)

            elif item == "previous":
                for prev in values:
                    previous = {}
                    for k, v in prev.items():
                        match k:
                            case "firstNameBeforeChange":
                                previous["firstname"] = v
                            case "lastNameBeforeChange":
                                previous["surname"] = v
                            case "midNameBeforeChange":
                                previous["patronymic"] = v
                            case "yearOfChange":
                                previous["changed"] = v
                            case "reason":
                                previous["reason"] = v
                    json_data["previous"].append(previous)

            elif item == "education":
                for edu in values:
                    education = {}
                    for k, v in edu.items():
                        match k:
                            case "educationType":
                                education["view"] = v
                            case "institutionName":
                                education["institution"] = v
                            case "endYear":
                                education["finished"] = v
                            case "specialty":
                                education["speciality"] = v
                    json_data["educations"].append(education)

            elif item == "experience":
                for exp in values:
                    work = {}
                    for key, value in exp.items():
                        match key:
                            case "beginDate":
                                work["starts"] = datetime.strptime(
                                    value, "%Y-%m-%d"
                                ).date()
                            case "endDate":
                                work["finished"] = datetime.strptime(
                                    value, "%Y-%m-%d"
                                ).date()
                            case "currentJob":
                                work["now_work"] = bool(value)
                            case "name":
                                work["workplace"] = value
                            case "address":
                                work["addresses"] = value
                            case "position":
                                work["position"] = value
                            case "fireReason":
                                work["reason"] = value
                    json_data["workplaces"].append(work)
    return (
        json_data
        if json_data["resume"]["surname"]
        and json_data["resume"]["firstname"]
        and json_data["resume"]["birthday"]
        else None
    )
