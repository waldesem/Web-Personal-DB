import { drizzle } from "db0/integrations/drizzle";
import { like } from "drizzle-orm";
import { db } from "~/server/db/index";
import { users } from "~/server/db/src/schema";

export default defineEventHandler(async (event) => {
  const search = getQuery(event).search as string;
  const drizzleDb = drizzle(db);
  let query = drizzleDb.select().from(users).$dynamic();
  if (search && search.length > 2) {
    if (search.match(/^[a-zA-Z_]+$/)) {
      query = query.where(like(users.username, `%${search}%`));
    } else {
      query = query.where(like(users.fullname, `%${search}%`));
    }
  }
  const results = await query.all();
  return results;
});
