export default defineEventHandler(async (event) => {
  const db = useDatabase();

  const body = await readBody(event) as object;
  
  Object.assign(body, {
    username: body.username.toLowerCase(),
    email: body.email.toLowerCase(),
    fullname: body.fullname,
    password: createPasswordHash("88888888"),
    change_pswd: 1,
    blocked: 0,
    deleted: 0,
    role: "user",
  });

  try {
    const stmt = db.prepare(`SELECT * FROM users WHERE username = ?`);
    if (stmt.get(body.username)) {
      return { message: "error" };
    } else {
      const stmt = db.prepare(
        `INSERT INTO users (${Object.keys(body).join(", ")}) VALUES (${"?"
          .repeat(Object.keys(body).length)
          .split("")
          .join(", ")})`
      );
      await stmt.run(...Object.values(body));
    }
    return { message: "success" };
  } catch (error) {
    console.error(error);
    return { message: "error" };
  }
});
