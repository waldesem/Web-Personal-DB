import { drizzle } from "db0/integrations/drizzle";
import { db } from "~/server/db/index";
import { users } from "~/server/db/src/schema";

export default defineEventHandler(async (event) => {
  const data = await readBody(event);
  const drizzleDb = drizzle(db);
  try {
    const resut = await drizzleDb
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
