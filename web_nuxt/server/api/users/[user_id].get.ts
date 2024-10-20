import { eq } from "drizzle-orm";
import { db } from "~/server/db/index";
import { users } from "~/server/db/src/schema";
import { createPasswordHash, Roles, Regions } from "~/server/utils";

export default defineEventHandler(async (event) => {
  const user_id = parseInt(getRouterParam(event, "user_id") as string);
  const item = getQuery(event).item as string;
  const results = await db.select().from(users).where(eq(users.id, user_id));
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
    });
  }
  if (item == "block") {
    Object.assign(user, { blocked: !user.blocked });
  } else if (item == "delete") {
    Object.assign(user, { deleted: !user.deleted });
  } else if (Object.values(Roles).includes(item)) {
    Object.assign(user, { role: item });
  } else if (Object.keys(Regions).includes(item)) {
    Object.assign(user, { region: Regions[item as keyof typeof Regions] });
  }
  try {
    await db.update(users).set(user).where(eq(users.id, user_id)).execute();
    return { message: "success" };
  } catch (error) {
    return { error: error };
  }
});
