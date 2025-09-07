export default defineEventHandler(async (event) => {
  const db = useDatabase();

  const personId = parseInt(getRouterParam(event, "personId") as string);
  try {
    const stmt = db.prepare(
      `UPDATE persons SET user_id = ?, editable = NOT editable WHERE id = ?`
    );
    await stmt.run(["", personId]);
  } catch (error) {
    console.error(error);
    return {
      message: "error",
    };
  }
});
