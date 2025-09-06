export default defineEventHandler(async (event) => {
  const db = useDatabase();

  const itemId = getRouterParam(event, "id");
  const item = getRouterParam(event, "item");

  if (item !== "persons") {
    const stmt = db.prepare(`SELECT * FROM ${item} WHERE person_id = ?`);
    return await stmt.all(itemId);
  } else {
    const stmt = db.prepare(`SELECT * FROM ${item} WHERE id = ?`);
    return await stmt.get(itemId);
  }
});
