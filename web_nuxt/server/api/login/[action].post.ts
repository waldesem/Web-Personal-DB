import { drizzle } from "db0/integrations/drizzle";
import { like } from "drizzle-orm";
import { db } from "~/server/db/index";
import { users } from "~/server/db/src/schema";
import {
  JWT_SECRET_KEY,
  checkPasswordHash,
  createPasswordHash,
  createJwtToken,
} from "~/server/utils";

export default defineEventHandler(async (event) => {
  const action = getRouterParam(event, "action");
  const json_data = await readBody(event);
  const drizzleDb = drizzle(db);
  const query = drizzleDb
    .select()
    .from(users)
    .where(like(users.username, `%${json_data["username"]}%`));
  const results = await query.all();
  const user = results[0];
  if (!user || user.blocked || user.deleted) {
    return { message: "Invalid" };
  }
  if (!checkPasswordHash(json_data["password"], user.passhash)) {
    if (user.attempt < 5) {
      user.attempt += 1;
    } else {
      user.blocked = true;
      return { message: "Invalid" };
    }
  }
  if (action == "update") {
    user.attempt = 0;
    user.change_pswd = false;
    user.passhash = createPasswordHash(json_data["password"]);
    return { message: "Updated" };
  }

  const delta = new Date().getTime() - user.pswd_create.getTime();
  if (delta > 86400000) {
    user.attempt = 0;
    const token = createJwtToken(user, JWT_SECRET_KEY);
    const session = await useSession(event, {
      password: SECRET_KEY",
    });
    await session.update({...user});
    if (token) {
      return { message: "Success", user_token: token };
    }
  }
  return { message: "Denied" };
});
