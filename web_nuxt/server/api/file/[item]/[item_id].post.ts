import fs from "node:fs";
import path from "node:path";
import sharp from "sharp";
import { eq } from "drizzle-orm";
import { db } from "~/server/db/index";
import { persons } from "~/server/db/src/schema";
import { makeDestinationFolder } from "~/server/utils";

export default defineEventHandler(async (event) => {
  const item = getRouterParam(event, "item") as string;
  const item_id = parseInt(getRouterParam(event, "item_id") as string);
  const files = await readBody(event);
  const results = await db
    .select()
    .from(persons)
    .where(eq(persons.id, item_id));
  if (results.length == 0) {
    return { message: "error" };
  }
  const person = results[0];
  if (!person.destination || !fs.existsSync(person.destination)) {
    const folderName = makeDestinationFolder(
      'current_user.get("region")',
      person.id.toString(),
      person.surname,
      person.firstname,
      person.patronymic || ""
    );
    Object.assign(person, { destination: folderName });
    await db
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
