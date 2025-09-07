import type { User, Login } from "~/server/types";

export default defineEventHandler(async (event) => {
  const db = useDatabase();

  const body = (await readBody(event)) as Login;
  const action = getQuery(event).action as string;

  try {
    const stmt = db.prepare(`SELECT * FROM users WHERE username = ?`);
    const user = stmt.get(body.username) as User;

    if (!user || user.deleted || user.blocked) {
      return { message: "invalid" };
    }

    if (!checkPasswordHash(body.password, user.passhash)) {
      if (user.attempt < 3) {
        await db.run(`UPDATE users SET attempt = attempt + 1 WHERE id = ?`, [
          user.id,
        ]);
        return { message: "invalid" };
      } else {
        await db.run(`UPDATE users SET attempt = 0, blocked = 1 WHERE id = ?`, [
          user.id,
        ]);
      }
    }

    if (action === "update" && body.new_pswd) {
      db.run(
        `UPDATE users SET password = ?, pswd_create = ?, change_pswd = 0, attempt = 0 WHERE id = ?`,
        [createPasswordHash(body.new_pswd), new Date(), user.id]
      );
    }

    const delta = new Date().getTime() - user.pswd_create.getTime();
    if (delta < 1000 * 60 * 60 * 24 * 365 && !user.change_pswd) {
      await db.run(`UPDATE users SET attempt = 0 WHERE id = ?`);
      return {
        message: "success",
        access_token: "createJWT",
        refresh_token: "createJWT",
      };
    }
  } catch (error) {
    console.error(error);
    return { message: "invalid" };
  }
});
