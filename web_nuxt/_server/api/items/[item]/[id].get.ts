export default defineEventHandler(async (event) => {
  const db = useDatabase();

  const itemId = getRouterParam(event, "id");
  const item = getRouterParam(event, "item");

  const stmt = db.prepare(`SELECT * FROM ${item} WHERE person_id = ?`);
  return await stmt.get(itemId);
});
