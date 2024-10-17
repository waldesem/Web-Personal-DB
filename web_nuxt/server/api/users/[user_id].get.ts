import { drizzle } from "db0/integrations/drizzle";
import { eq } from "drizzle-orm";
import { db } from "~/server/db/index";
import { users } from "~/server/db/src/schema";
import { createPasswordHash, Roles, Regions } from "~/server/utils";

export default defineEventHandler(async (event) => {
  const user_id = parseInt(getRouterParam(event, "user_id") as string);
  const item = getQuery(event).item as string;
  const drizzleDb = drizzle(db);
  const query = drizzleDb.select().from(users).where(eq(users.id, user_id));
  const results = await query.all();
  if (results.length == 0) {
    return { message: "error" };
  }
  const user = results[0];
  if (item == "drop") {
    Object.assign(user, {
      passhash: createPasswordHash("88888888"),
      attempt: 0,
      blocked: false,
      change_pswd: true,
    })
  }
  if (item == "block") {
    Object.assign(user, { blocked: !user.blocked });
  } else if (item == "delete") {
    Object.assign(user, { deleted: !user.deleted });
  } else if (Object.values(Roles).includes(item)) {
    Object.assign(user, { roles: item });
  } else if (Object.values(Regions).includes(item)) {
    Object.assign(user, { regions: item });
  }
  try {
    await drizzleDb
      .update(users)
      .set(user)
      .where(eq(users.id, user_id));
    return { message: "success" };
  } catch (error) {
    return { error: error };
  }
});