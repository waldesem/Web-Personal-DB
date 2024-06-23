import sqlite3
from config import Config

from typing import Optional
from pydantic import BaseModel

from app.models.models import *


class People(BaseModel):
    person: Person
    staffs: Optional[Staff] = None
    previous: Optional[Prev] = None
    documents: Optional[Document] = None
    addresses: Optional[Address] = None
    contacts: Optional[Contact] = None
    educations: Optional[Education] = None
    workplaces: Optional[Workplace] = None
    affilations: Optional[Affilation] = None
    relations: Optional[Relation] = None
    checks: Optional[Check] = None
    investigations: Optional[Investigation] = None
    poligrafs: Optional[Poligraf] = None
    inquiries: Optional[Inquiry] = None
    connects: Optional[Connects] = None


stmt = """
    SELECT *
    FROM persons
    LEFT JOIN staffs ON persons.id = staffs.person_id
    LEFT JOIN previous ON persons.id = previouss.person_id
    LEFT JOIN documents ON persons.id = documents.person_id
    LEFT JOIN addresses ON persons.id = addresses.person_id
    LEFT JOIN contacts ON persons.id = contacts.person_id
    LEFT JOIN educations ON persons.id = educations.person_id
    LEFT JOIN workplaces ON persons.id = workplaces.person_id
    LEFT JOIN affilations ON persons.id = affilations.person_id
    LEFT JOIN relations ON persons.id = relations.person_id
    LEFT JOIN checks ON persons.id = checks.person_id
    LEFT JOIN investigations ON persons.id = investigations.person_id
    LEFT JOIN poligrafs ON persons.id = poligrafs.person_id
    LEFT JOIN inquiries ON persons.id = inquiries.person_id
    LEFT JOIN connects ON persons.id = connects.person_id
    WHERE persons.id = ?
"""

def select(query, many=False, args=None):
    with sqlite3.connect(Config.DATABASE_URI, timeout=1) as con:
        cursor = con.cursor()
        try:
            cursor.execute(query, args) if args else cursor.execute(query)
            result = cursor.fetchall() if many else cursor.fetchone()

            if result:
                columns = [desc[0] for desc in cursor.description]
                if many:
                    return [dict(zip(columns, res)) for res in result]
                return dict(zip(columns, result))

            return [] if many else None

        except sqlite3.Error as e:
            print(f"Error: {e}")
            con.rollback()


result = select(stmt, args=(1,))

print(result)