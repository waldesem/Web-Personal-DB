export default defineEventHandler(async (event) => {
  const db = useDatabase();

  const user_id = parseInt(getRouterParam(event, "user_id") as string);
  const action = getQuery(event).action as string;

  try {
    if (action === "delete") {
      await db.run(`UPDATE users SET deleted = NOT deleted WHERE id = ?`, [
        user_id,
      ]);
    } else if (action === "block") {
      await db.run(`UPDATE users SET blocked = NOT blocked WHERE id = ?`, [
        user_id,
      ]);
    } else if (action === "reset") {
      await db.run(
        `UPDATE users SET password = ? blocked = 0, change_pswd = 1 WHERE id = ?`,
        [createPasswordHash("88888888"), user_id]
      );
    } else {
      await db.run(`UPDATE users SET role = ? WHERE id = ?`, [action, user_id]);
    }
    return { message: "success" };
  } catch (error) {
    console.error(error);
    return {
      message: "error",
    };
  }
});
