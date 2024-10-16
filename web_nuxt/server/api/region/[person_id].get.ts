import fs from "node:fs";
import path from 'node:path';

import { drizzle } from "db0/integrations/drizzle";
import { eq } from "drizzle-orm";
import { db } from "~/server/db/index";
import { persons } from "~/server/db/src/schema";

export default defineEventHandler(async (event) => {
  const person_id = parseInt(getRouterParam(event, "person_id") as string);
  const region = getQuery(event).region as string;
  const drizzleDb = drizzle(db);
  const query = drizzleDb
    .select()
    .from(persons)
    .where(eq(persons.id, person_id));
  const results = await query.all();
  if (results.length == 0) {
    return { message: "error" };
  }
  const person = results[0];
  const folderName = path.join(
    region, person.surname[0], `${person.id}-${person.surname} ${person.firstname} ${person.patronymic}`
  );
  try {
    if (!fs.existsSync(folderName)) {
      fs.mkdirSync(folderName);
    }
  } catch (err) {
    return {"message": err};
  }
  if (person.destination) {
    try {
      fs.cpSync(person.destination, folderName);
    } catch (err) {
      return {"message": err};
    }
  }
  try {
    drizzleDb
      .update(persons)
      .set({ destination: folderName, editable: false })
      .where(eq(persons.id, person_id));
    await query.run();
    return {"message": "success"};
  } catch (err) {
    return {"message": err};
  }
});
