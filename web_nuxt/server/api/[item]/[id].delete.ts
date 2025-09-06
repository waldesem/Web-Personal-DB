export default defineEventHandler(async (event) => {
  const db = useDatabase();

  const itemId = getRouterParam(event, "id");
  const item = getRouterParam(event, "item");

  const stmt = db.prepare(`DELETE FROM ${item} WHERE id = ?`);
  await stmt.run(itemId);

  return {
    message: "success",
  };
});
