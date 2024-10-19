import fs from "node:fs";
import path from "node:path";
import { and, ilike, eq } from "drizzle-orm";
import { db } from "~/server/db/index";
import { persons } from "~/server/db/src/schema";
import { makeDestinationFolder } from "~/server/utils";

export default defineEventHandler(async (event) => {
  const data = await readBody(event);
  const results = await db
    .select()
    .from(persons)
    .where(
      and(
        ilike(persons.surname, data.surname),
        ilike(persons.firstname, data.firstname),
        ilike(persons.patronymic, data.patronymic),
        eq(persons.birthday, data.birthday)
      )
    );
  if (results.length == 0) {
    Object.assign(data, {
      editable: true,
      user_id: "event.context.user.id",
      region: "event.context.user.region",
    });
    const personId = await db
      .insert(persons)
      .values(data)
      .onConflictDoNothing()
      .returning()
      .then((rows) => rows[0].id);
    const folderName = makeDestinationFolder(
      data.region,
      data.id,
      data.surname,
      data.firstname,
      data.patronymic
    );
    await db.update(persons).set({ destination: folderName }).execute();
    return { person_id: personId };
  }
  const person = results[0];
  if (!person.destination || !fs.existsSync(person.destination)) {
    return { person_id: null };
  }
  const folderName = path.join(
    "event.context.user.region",
    data.surname[0],
    `${data.id}-${data.surname} ${data.firstname} ${data.patronymic}`
  );
  if (!fs.existsSync(folderName)) {
    fs.mkdirSync(folderName);
  }
  if (data.region != person.region) {
    try {
      fs.cpSync(person.destination, folderName);
    } catch (err) {
      console.error(err);
    }
  }
  Object.assign(person, { destination: folderName, id: person.id });
  try {
    await db
      .update(persons)
      .set({ ...data, destination: folderName })
      .where(eq(persons.id, person.id))
      .execute();
  } catch (err) {
    return { person_id: null, message: err };
  }
  return { person_id: person.id };
});
