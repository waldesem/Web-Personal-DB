from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
import os
from os.path import basename
import smtplib

from flask import abort, current_app
from PIL import Image
from pydantic import ValidationError
from sqlalchemy import desc, select

from ..depends.depend import current_user
from ..model.models import AnketaSchemaJson
from ..model.tables import Users, db_session, Persons, tables_models


def handle_get_item(item, item_id):
    """
    Retrieves an item from the database based on the provided item and item_id.

    Args:
        item (str): The type of item to retrieve.
        item_id (int): The ID of the item to retrieve.

    Returns:
        dict or list: If item is "persons", a dictionary containing the item's data and the associated user's fullname.
                      Otherwise, a list of dictionaries containing the item's data and the associated user's fullname,
                      ordered by descending item ID.
    Raises:
        None
    """
    if item in ['persons', 'checks', 'poligrafs', 'inquiries', 'investigations']:
        stmt = select(tables_models[item], Users.fullname)
        if item == "persons":
        stmt = stmt.filter(Persons.id == item_id)
        else:
        stmt = stmt.filter(tables_models[item].person_id == item_id)
    stmt = stmt.filter(
        tables_models[item].user_id == Users.id
    )
        query = db_session.execute(stmt).order_by(
    desc(tables_models[item].id)
    ).all()
        result = [row[0].to_dict() | {"username": row[1]} for row in query]
        return result[0] if item == "persons" else result
    else:
        query = select(tables_models[item]).filter(tables_models[item].person_id == item_id).order_by(
    desc(tables_models[item].id)
    ).all()
        return[row[0].to_dict() for row in query]


def handle_post_resume(resume):
    """
    Updates a resume in the database with the provided data.

    Args:
        data (dict): A dictionary containing the resume data.

    Returns:
        int: The ID of the updated resume.

    Raises:
        Exception: If there is an error updating the resume.

    """
    resume["editable"] = True
    resume["user_id"] = current_user["id"]
    resume["region"] = current_user["region"]
    if not resume.get("id"):
        person = db_session.execute(
            select(Persons).where(
                Persons.surname.ilike("%{}%".format(resume["surname"])),
                Persons.firstname.ilike("%{}%".format(resume["firstname"])),
                Persons.patronymic.ilike("%{}%".format(resume["patronymic"])),
                Persons.birthday == resume["birthday"],
            )
        ).scalar_one_or_none()
        if not person:
            person = Persons(**resume)
            db_session.add(person)
            db_session.flush()
            person.destination = make_destination(
                resume["region"],
                resume["surname"],
                resume["firstname"],
                resume.get("patronymic", ""),
                person.id,
            )
            db_session.commit()                
            return [person.id, person.destination]
        else:
            if person.user_id != current_user["id"]:
                return abort(400)
            resume["id"] = person.id
            handle_post_item(resume, "persons")
            return [resume["id"], person.destination]
    handle_post_item(resume, "persons")


def handle_post_item(json_dict, item, item_id=""):
    """
    Updates an item in the database based on the provided JSON data, item, and item_id.

    Args:
        json_data (dict): A dictionary containing the data to update the item.
        item (str): The type of item to update in the database.
        item_id (int): The ID of the item to update.

    Returns:
        None
    """
    if item != "persons":
        json_dict["person_id"] = item_id
        json_dict["user_id"] = current_user["id"]
    db_session.merge(tables_models[item](**json_dict))
    db_session.commit()


def handle_json_to_dict(data):
    try:
        anketa = AnketaSchemaJson(**data).dict()
        anketa["resume"] = {
            "region": current_user["region"],
            "surname": anketa.pop("surname", "").upper().strip(),
            "firstname": anketa.pop("firstname", "").upper().strip(),
            "patronymic": anketa.pop("patronymic", "").upper().strip()
            if anketa.get("patronymic")
            else "",
            "birthday": anketa.pop("birthday", ""),
            "birthplace": anketa.pop("birthplace", ""),
            "citizenship": anketa.pop("citizenship", ""),
            "dual": anketa.pop("dual", ""),
            "marital": anketa.pop("marital", ""),
            "inn": anketa.pop("inn", ""),
            "snils": anketa.pop("snils", ""),
        }
        anketa["staffs"].append(
            {
                "position": anketa.pop("positionName", ""),
                "department": anketa.pop("department", ""),
            }
        )
        anketa["documents"].append(
            {
                "view": "Паспорт",
                "digits": anketa.pop("passportNumber", ""),
                "series": anketa.pop("passportSerial", ""),
                "issue": anketa.pop("passportIssueDate", ""),
                "agency": anketa.pop("passportIssuedBy", ""),
            }
        )
        anketa["addresses"].extend(
            [
                {
                    "view": "Адрес проживания",
                    "addresses": anketa.pop("validAddress", ""),
                },
                {
                    "view": "Адрес регистрации",
                    "addresses": anketa.pop("regAddress", ""),
                },
            ]
        )
        anketa["contacts"].extend(
            [
                {"view": "Телефон", "contact": anketa.pop("contactPhone", "")},
                {"view": "Электронная почта", "contact": anketa.pop("email", "")},
            ]
        )
        anketa["affilations"].extend(
            anketa.pop("organizations")
            + anketa.pop("stateOrganizations")
            + anketa.pop("publicOfficeOrganizations")
            + anketa.pop("relatedPersonsOrganizations")
        )
        return anketa
    except ValidationError as e:
        print(e)
        return None


def handle_image(file, item_dir):
    """
    Opens a file, reads the image data, saves it to a new file in a specified directory.

    Args:
        file (str): The path to the file containing the image.
        item_dir (str): The directory where the new image file will be saved.

    Returns:
        None
    """
    image = Image.open(file)
    image = image.convert("RGB")
    new_file = os.path.join(item_dir, "image.jpg")
    if os.path.isfile(new_file):
        os.remove(new_file)
    image.save(new_file, format="JPEG", quality=90)


def make_destination(region, surname, firstname, patronymic, person_id):
    """
    Generate the destination directory path for a given set of parameters.

    Args:
        region (str): The region of the destination directory.
        surname (str): The surname of the person.
        firstname (str): The firstname of the person.
        patronymic (str): The patronymic of the person.
        person_id (str): The unique identifier of the person.

    Returns:
        str: The full path of the destination directory.

    Raises:
        None
    """
    destination = os.path.join(
        current_app.config["BASE_PATH"],
        region,
        surname[0],
        f"{person_id}-{surname} {firstname} "
        f"{patronymic if patronymic else ''}".rstrip(),
    )
    if not os.path.isdir(destination):
        os.mkdir(destination)
    return destination


def mail_handler(
    send_from: str, send_to: list, subject: str, body: str, server: str, file=None
):
    msg = MIMEMultipart()
    msg["From"] = send_from
    msg["To"] = ",".join(send_to)
    msg["Date"] = formatdate(localtime=True)
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    if file:
        with open(file, "rb") as f:
            part = MIMEApplication(f.read(), Name=basename(f))

            part["Content-Disposition"] = 'attachment; filename="%s"' % basename(f)

            msg.attach(part)

    smtp = smtplib.SMTP(server)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()
