export default defineEventHandler(async (event) => {
  const db = useDatabase();

  const itemId = getRouterParam(event, "id");

  try {
    const stmt = db.prepare(`DELETE FROM persons WHERE id = ?`);
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
