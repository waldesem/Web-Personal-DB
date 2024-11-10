def json_to_dict(json_dict: dict):
    """
    Transforms a JSON-dictionary into a python-dictionary.

    :param json_dict: A JSON-dictionary
    :return: A python-dictionary
    """
    return {
        "resume": {
            "surname": json_dict.get("lastName"),
            "firstname": json_dict.get("firstName"),
            "patronymic": json_dict.get("midName"),
            "birthday": json_dict.get("birthday"),
            "birthplace": json_dict.get("birthplace"),
            "citizenship": json_dict.get("citizen"),
            "dual": json_dict.get("additionalCitizenship"),
            "marital": json_dict.get("maritalStatus"),
            "inn": json_dict.get("inn"),
            "snils": json_dict.get("snils"),
        },
        "staffs": [
            {
                "position": json_dict.get("positionName"),
                "department": json_dict.get("department"),
            }
        ],
        "documents": [
            {
                "view": "Паспорт",
                "digits": json_dict.get("passportNumber"),
                "series": json_dict.get("passportSerial"),
                "issue": json_dict.get("passportIssueDate"),
                "agency": json_dict.get("passportIssuedBy"),
            }
        ],
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
        "educations": [
            {
                "view": edu.get("educationType"),
                "institution": edu.get("institutionName"),
                "finished": edu.get("endYear"),
                "specialty": edu.get("specialty"),
            }
            for edu in json_dict.get("education")
            if json_dict.get("education")
        ],
        "workplaces": [
            {
                "starts": work.get("beginDate"),
                "finished": work.get("endDate"),
                "now_work": work.get("currentJob"),
                "workplace": work.get("name"),
                "addresses": work.get("address"),
                "reason": work.get("fireReason"),
                "position": work.get("position"),
            }
            for work in json_dict.get("experience")
            if json_dict.get("experience")
        ],
        "previous": [
            {
                "firstname": prev.get("firstNameBeforeChange"),
                "surname": prev.get("lastNameBeforeChange"),
                "patronymic": prev.get("midNameBeforeChange"),
                "changed": prev.get("yearOfChange"),
                "reason": prev.get("reason"),
            }
            for prev in json_dict.get("nameWasChanged")
            if json_dict.get("nameWasChanged")
        ],
        "affilations": (
            [
                {
                    "view": "Участвует в деятельности коммерческих организаций",
                    "organization": aff.get("name"),
                    "inn": aff.get("inn"),
                }
                for aff in json_dict.get("organizations")
                if json_dict.get("organizations")
            ]
            + [
                {
                    "view": "Являлся государственным должностным лицом",
                    "organization": aff.get("name"),
                }
                for aff in json_dict.get("stateOrganizations")
                if json_dict.get("stateOrganizations")
            ]
            + [
                {
                    "view": "Связанные лица работают в государственных организациях",
                    "organization": aff.get("name"),
                }
                for aff in json_dict.get("relatedPersonsOrganizations")
                if json_dict.get("relatedPersonsOrganizations")
            ]
            + [
                {
                    "view": "Являлся государственным или муниципальным служащим",
                    "organization": aff.get("name"),
                }
                for aff in json_dict.get("publicOfficeOrganizations")
                if json_dict.get("publicOfficeOrganizations")
            ]
        ),
    }

