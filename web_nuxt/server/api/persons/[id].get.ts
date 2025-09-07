export default defineEventHandler(async (event) => {
  const db = useDatabase();

  const itemId = getRouterParam(event, "id");
  const item = getRouterParam(event, "item");

  const stmt = db.prepare(`SELECT * FROM ${item} WHERE id = ?`);
  return await stmt.get(itemId);
});
