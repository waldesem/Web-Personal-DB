export default defineEventHandler(async (event) => {
  const db = useDatabase();

  const itemId = getRouterParam(event, "id");
  const item = getRouterParam(event, "item");

  try {
    const stmt = db.prepare(`DELETE FROM ${item} WHERE id = ?`);
    await stmt.run(itemId);

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
