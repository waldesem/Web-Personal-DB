import { db } from "~/server/db/index";
import { users } from "~/server/db/src/schema";

export default defineEventHandler(async (event) => {
  const data = await readBody(event);
  try {
    const resut = await db
      .insert(users)
      .values(data)
      .onConflictDoNothing({
        target: users.username,
      })
      .returning();
    if (resut.length == 0) {
      return { message: "error" };
    }
  } catch (error) {
    return { error: error };
  }
  return { message: "success" };
});
