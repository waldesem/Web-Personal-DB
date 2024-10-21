import fs from "node:fs";
import { and, ilike, eq } from "drizzle-orm";
import { db } from "~/server/db/index";
import { persons } from "~/server/db/src/schema";
import { makeDestinationFolder, currentUser } from "~/server/utils";

export default defineEventHandler(async (event) => {
  const data = await readBody(event);
  const curUser = await currentUser();
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
      user_id: curUser.id,
      region: curUser.region,
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
    await db
      .update(persons)
      .set({ destination: folderName })
      .where(eq(persons.id, personId));
    return { person_id: personId };
  }
  const person = results[0];
  if (person.editable) {
    return { person_id: null };
  }
  const folderName = makeDestinationFolder(
    curUser.region,
    person.id.toString(),
    person.surname,
    person.firstname,
    person.patronymic || ""
  );
  if (!fs.existsSync(folderName)) {
    fs.mkdirSync(folderName);
  }
  if (data.region != person.region) {
    if (person.destination) {
      fs.cpSync(person.destination, folderName);
    }
  }
  Object.assign(person, { destination: folderName, id: person.id });
  await db
    .update(persons)
    .set({ ...data, destination: folderName })
    .where(eq(persons.id, person.id));
  return { person_id: person.id };
});
