import fs from "node:fs";
import path from "node:path";

export default defineEventHandler(async (event) => {
  const db = useDatabase();

  const item_id = parseInt(getRouterParam(event, "person_id") as string);
  const files = await readBody(event);

  const stmt = db.prepare(`SELECT * FROM persons WHERE id = ?`);
  const person = stmt.get([item_id]);

  let folderName = person.destination;

  if (!person.destination || !fs.existsSync(person.destination)) {
    folderName = makeDestinationFolder(
      person.id.toString(),
      person.surname,
      person.firstname,
      person.patronymic ?? ""
    );
    await db.run(`UPDATE persons SET destination = ? WHERE id = ?`, [
      path.join(folderName),
    ]);
  }
  const dateFolder = path.join(
      folderName,
      `${new Date().toLocaleDateString()}`
  );
  if (!fs.existsSync(dateFolder)) {
      fs.mkdirSync(dateFolder);
  }
  fs.writeFileSync(path.join(dateFolder), files.file);
  return { message: "success" };
});
