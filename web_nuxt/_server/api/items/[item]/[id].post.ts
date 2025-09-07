export default defineEventHandler(async (event) => {
  const db = useDatabase();

  const itemId = getRouterParam(event, "id") as string;
  const item = getRouterParam(event, "item") as string;
  const body = ((await readBody(event)) + { person_id: itemId }) as object;

  try {
    if (body["id" as keyof typeof body]) {
      const stmt = db.prepare(
        `UPDATE ${item} SET ${Object.entries(body)
          .map(([key, _]) => `${key} = ?`)
          .join(", ")} WHERE id = ?`
      );
      await stmt.run(...Object.values(body), itemId);
    } else {
      const stmt = db.prepare(
        `INSERT INTO ${item} (${Object.keys(body).join(", ")}) VALUES (${"?"
          .repeat(Object.keys(body).length)
          .split("")
          .join(", ")})`
      );
      await stmt.run(...Object.values(body));
    }
    return {
      message: "success",
    };
  } catch (e) {
    console.error(e);
    return {
      message: "error",
    };
  }
});
