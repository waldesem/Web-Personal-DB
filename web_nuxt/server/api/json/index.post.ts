import fs from "node:fs";
import path from "node:path";
import { drizzle } from "db0/integrations/drizzle";
import { and, ilike, eq } from "drizzle-orm";
import { db } from "~/server/db/index";
import {
  itemsInsertModels,
  itemsTables,
  persons,
} from "~/server/db/src/schema";
import { anketaSchemaJson } from "~/server/schema";

export default defineEventHandler(async (event) => {
  const files = await readBody(event);
  const reader = new FileReader();
  reader.readAsText(files[0].file);
  try {
    const jsonData = await new Promise((resolve) => {
      reader.onload = () => {
        resolve(JSON.parse(reader.result as string));
      };
    });
    const validated = anketaSchemaJson.parse(jsonData);
    const anketa = {
      resume: {
        region: "current_user",
        surname: validated.lastName,
        firstname: validated.firstName,
        patronymic: validated.midName,
        birthday: validated.birthday,
        birthplace: validated.birthplace,
        citizenship: validated.citizen,
        dual: validated.additionalCitizenship,
        marital: validated.maritalStatus,
        inn: validated.inn,
        snils: validated.snils,
      },
      staffs: [
        {
          position: validated.positionName,
          department: validated.department,
        },
      ],
      documents: [
        {
          view: "Паспорт",
          series: validated.passportSerial,
          digits: validated.passportNumber,
          agency: validated.passportIssuedBy,
          issue: validated.passportIssueDate,
          created: Date.now(),
        },
      ],
      addresses: [
        {
          view: "Адрес регистрации",
          address: validated.regAddress,
          created: Date.now(),
        },
        {
          view: "Адрес проживания",
          address: validated.validAddress,
        },
      ],
      contacts: [
        {
          view: "Адрес электронной почты",
          contact: validated.email,
        },
        {
          view: "Мобильный телефон",
          contact: validated.contactPhone,
        },
      ],
      previous: [],
      educations: [],
      workplaces: [],
      affilations: [],
    };
    for (const prev of validated.previous) {
      Object.assign(anketa.previous, [
        {
          firstname: prev.firstNameBeforeChange,
          surname: prev.lastNameBeforeChange,
          patronymic: prev.midNameBeforeChange,
          changed: prev.yearOfChange,
          reason: prev.reason,
        },
      ]);
    }
    for (const education of validated.educations) {
      Object.assign(anketa.educations, [
        {
          view: education.educationType,
          institution: education.institutionName,
          finished: education.endYear,
          specialty: education.specialty,
        },
      ]);
    }
    for (const work of validated.workplaces) {
      Object.assign(anketa.workplaces, [
        {
          starts: work.beginDate,
          finished: work.endDate,
          now_work: work.currentJob,
          workplace: work.name,
          addresses: work.address,
          position: work.position,
          reason: work.fireReason,
        },
      ]);
    }
    for (const aff of validated.organizations) {
      Object.assign(anketa.affilations, [
        {
          view: aff.view,
          organization: aff.name,
          inn: aff.inn,
        },
      ]);
    }
    for (const aff of validated.relatedPersonsOrganizations) {
      Object.assign(anketa.affilations, [
        {
          view: aff.view,
          organization: aff.name,
          inn: aff.inn,
        },
      ]);
    }
    for (const aff of validated.stateOrganizations) {
      Object.assign(anketa.affilations, [
        {
          view: aff.view,
          organization: aff.name,
        },
      ]);
    }
    for (const aff of validated.publicOfficeOrganizations) {
      Object.assign(anketa.affilations, [
        {
          view: aff.view,
          organization: aff.name,
        },
      ]);
    }
    const drizzleDb = drizzle(db);
    const query = drizzleDb
      .select()
      .from(persons)
      .where(
        and(
          ilike(persons.surname, anketa.resume.surname),
          ilike(persons.firstname, anketa.resume.firstname),
          ilike(persons.patronymic, anketa.resume.patronymic || "%%"),
          eq(persons.birthday, anketa.resume.birthday)
        )
      );
    const results = await query.all();
    const validResume = itemsInsertModels["persons"].parse(anketa.resume);
    if (results.length == 0) {
      Object.assign(anketa.resume, {
        editable: true,
        user_id: "event.context.user.id",
        region: "event.context.user.region",
      });
      const personId = await drizzleDb
        .insert(persons)
        .values(validResume)
        .onConflictDoNothing()
        .returning()
        .then((rows) => rows[0].id);
      const folderName = path.join(
        "event.context.user.region",
        anketa.resume.surname[0],
        `${personId}-${anketa.resume.surname} ${anketa.resume.firstname} ${anketa.resume.patronymic}`
      );
      if (!fs.existsSync(folderName)) {
        fs.mkdirSync(folderName);
      }
      await drizzleDb
        .update(persons)
        .set({ destination: folderName })
        .execute();
      for (const [key, values] of Object.entries(anketa)) {
        const table = itemsTables[key as keyof typeof itemsTables];
        if (!table || key == "resume") continue;
        for (const value in values) {
          Object.assign(value, {
            person_id: personId,
            user_id: "current_user",
          });
          try {
            const validItem =
              itemsInsertModels[key as keyof typeof itemsInsertModels].parse(
                value
              );
            await drizzleDb.insert(table).values(validItem);
          } catch (error) {
            console.error(error);
          }
        }
      }
      return { person_id: personId };
    }
    const person = results[0];
    const folderName = path.join(
      "event.context.user.region",
      anketa.resume.surname[0],
      `${person.id}-${person.surname} ${person.firstname} ${person.patronymic}`
    );
    if (!fs.existsSync(folderName)) {
      fs.mkdirSync(folderName);
    }
    if (anketa.resume.region != person.region && person.destination) {
      try {
        fs.cpSync(person.destination, folderName);
      } catch (err) {
        console.error(err);
      }
    }
    Object.assign(person, { destination: folderName, id: person.id });
    try {
      await drizzleDb
        .update(persons)
        .set({ ...anketa.resume, destination: folderName })
        .where(eq(persons.id, person.id))
        .execute();
    } catch (err) {
      return { person_id: null, message: err };
    }
    for (const [key, values] of Object.entries(anketa)) {
      const table = itemsTables[key as keyof typeof itemsTables];
      if (!table || key == "resume") continue;
      for (const value in values) {
        Object.assign(value, {
          person_id: person.id,
          user_id: "current_user",
        });
        try {
          const validItem =
            itemsInsertModels[key as keyof typeof itemsInsertModels].parse(
              value
            );
          await drizzleDb.insert(table).values(validItem);
        } catch (error) {
          console.error(error);
        }
      }
    }
    return { person_id: person.id };
  } catch (error) {
    return { person_id: null, message: error };
  }
});
