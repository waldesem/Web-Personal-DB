import fs from "fs";
import path from "path";
import { db } from "~/server/db";
import { eq } from "drizzle-orm";
import { persons } from "~/server/db/src/schema";

export default defineEventHandler(async (event) => {
  const personId = parseInt(getRouterParam(event, "item_id") as string);
  const result = await db
    .select()
    .from(persons)
    .where(eq(persons.id, personId));
  if (result.length) {
    const person = result[0];
    const imagePath = path.join(
      person.destination as string,
      "image",
      "image.jpg"
    );
    if (fs.existsSync(imagePath)) {
      const buffer = fs.readFileSync(imagePath);
      return send(event, buffer, "image/jpeg");
    }
  }
  const buffer = fs.readFileSync("static/no-photo.png");
  return send(event, buffer, "image/jpeg");
});
