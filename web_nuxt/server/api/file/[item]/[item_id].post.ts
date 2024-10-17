import fs from "node:fs";
import path from "node:path";
import sharp from "sharp";
import { drizzle } from "db0/integrations/drizzle";
import { eq } from "drizzle-orm";
import { db } from "~/server/db/index";
import { persons } from "~/server/db/src/schema";

export default defineEventHandler(async (event) => {
  const item = getRouterParam(event, "item") as string;
  const item_id = parseInt(getRouterParam(event, "item_id") as string);
  const files = await readBody(event);
  const drizzleDb = drizzle(db);
  const query = drizzleDb.select().from(persons).where(eq(persons.id, item_id));
  const results = await query.all();
  if (results.length == 0) {
    return { message: "error" };
  }
  const person = results[0];
  if (!person.destination || !fs.existsSync(person.destination)) {
    const folderName = path.join(
      'current_user.get("region")',
      person.surname[0],
      `${person.id}-${person.surname} ${person.firstname} ${person.patronymic}`
    );
    try {
      if (!fs.existsSync(folderName)) {
        fs.mkdirSync(folderName);
      }
    } catch (err) {
      return { message: err };
    }
    Object.assign(person, { destination: folderName });
    const drizzleDb = drizzle(db);
    await drizzleDb
      .update(persons)
      .set({ destination: folderName })
      .where(eq(persons.id, item_id));
  }
  const itemFolder = path.join(person.destination as string, item);
  try {
    if (!fs.existsSync(itemFolder)) {
      fs.mkdirSync(itemFolder);
    }
  } catch (err) {
    return { message: err };
  }
  if (item == "image") {
    sharp(files[0])
      .resize()
      .jpeg({
        quality: 90,
        mozjpeg: true,
      })
      .toFormat("jpeg")
      .toFile(path.join(item, "image.jpg"))
      .then(() => {
        return true;
      })
      .catch((err) => {
        console.error(err);
        return false;
      });
  }
  const dateFolder = path.join(
    itemFolder,
    `${new Date().toLocaleDateString()}`
  );
  try {
    if (!fs.existsSync(dateFolder)) {
      fs.mkdirSync(dateFolder);
    }
  } catch (err) {
    return { message: err };
  }
  fs.writeFileSync(path.join(dateFolder, item), files.file);
  return { message: "success" };
});
