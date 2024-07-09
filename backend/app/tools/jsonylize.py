from datetime import datetime
import re

from ..depends.depend import current_user


def parse_json(json_dict: dict):
    """
    Parses a JSON dictionary and returns a dictionary with the parsed data.

    Args:
        json_dict (dict): The JSON dictionary to parse.

    Returns:
        dict: The parsed dictionary.
    """
    json_data = {
        "resume": {
            "region": current_user["region"],
            "firstname": json_dict.get("firstName"),
            "surname": json_dict.get("lastName"),
            "patronymic": json_dict.get("midName"),
            "birthday": datetime.strptime(json_dict["birthday"], "%Y-%m-%d").date()
            if json_dict.get("birthday")
            and re.match(r"^\d{4}-\d{2}-\d{2}$", json_dict["birthday"])
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
                "view": "Паспорт",
                "digits": json_dict.get("passportNumber"),
                "series": json_dict.get("passportSerial"),
                "issue": datetime.strptime(
                    json_dict["passportIssueDate"], "%Y-%m-%d"
                ).date()
                if json_dict.get("passportIssueDate")
                and re.match(r"^\d{4}-\d{2}-\d{2}$", json_dict["passportIssueDate"])
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
        "previous": [
            {
                "firstname": prev.get("firstNameBeforeChange"),
                "surname": prev.get("lastNameBeforeChange"),
                "patronymic": prev.get("midNameBeforeChange"),
                "changed": prev.get("yearOfChange"),
                "reason": prev.get("reason"),
            }
            for prev in json_dict.get("nameWasChanged", [])
        ],
        "educations": [
            {
                "view": edu.get("educationType"),
                "institution": edu.get("institutionName"),
                "finished": edu.get("endYear"),
                "speciality": edu.get("specialty"),
            }
            for edu in json_dict.get("education", [])
        ],
        "workplaces": [
            {
                "starts": datetime.strptime(exp["beginDate"], "%Y-%m-%d").date()
                if exp.get("beginDate")
                and re.match(r"^\d{4}-\d{2}-\d{2}$", exp["beginDate"])
                else None,
                "finished": datetime.strptime(exp["endDate"], "%Y-%m-%d").date()
                if exp.get("endDate")
                and re.match(r"^\d{4}-\d{2}-\d{2}$", exp["endDate"])
                else None,
                "now_work": True if exp.get("currentJob") else False,
                "workplace": exp.get("name"),
                "addresses": exp.get("address"),
                "position": exp.get("position"),
                "reason": exp.get("fireReason"),
            }
            for exp in json_dict.get("experience", [])
        ],
        "affilations": [],
    }
    views = {
        "publicOfficeOrganizations": "Являлся государственным или муниципальным служащим",
        "stateOrganizations": "Являлся государственным должностным лицом",
        "relatedPersonsOrganizations": "Связанные лица работают в государственных организациях",
        "organizations": "Участвует в деятельности коммерческих организаций",
    }
    for item, value in views.items():
        affils = json_dict.get(item, [])
        for org in affils:
            json_data["affilations"].append(
                {
                    "view": value,
                    "organization": org.get("name"),
                    "position": org.get("position"),
                    "inn": org.get("inn"),
                }
            )

    return (
        json_data
        if json_data["resume"]["surname"]
        and json_data["resume"]["firstname"]
        and json_data["resume"]["birthday"]
        else None
    )
