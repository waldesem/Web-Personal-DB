import { like } from "drizzle-orm";
import { db } from "~/server/db/index";
import { users } from "~/server/db/src/schema";

export default defineEventHandler(async (event) => {
  const search = getQuery(event).search as string;
  let query = db.select().from(users).$dynamic();
  if (search && search.length > 2) {
    if (search.match(/^[a-zA-Z_]+$/)) {
      query = query.where(like(users.username, `%${search}%`));
    } else {
      query = query.where(like(users.fullname, `%${search}%`));
    }
  }
  const results = await query.execute();
  return results;
});
