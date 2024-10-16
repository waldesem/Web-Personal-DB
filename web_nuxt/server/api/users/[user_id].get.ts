import { drizzle } from "db0/integrations/drizzle";
import { eq } from "drizzle-orm";
import { db } from "~/server/db/index";
import { users } from "~/server/db/src/schema";

export default defineEventHandler(async (event) => {
  const user_id = parseInt(getRouterParam(event, "user_id") as string);
  const item = getQuery(event).item;
  const drizzleDb = drizzle(db);
  const query = drizzleDb.select().from(users).where(eq(users.id, user_id));
  const results = await query.all();
  if (results.length == 0) {
    return { message: "error" };
  }
  const user = results[0];
  return user;
});
