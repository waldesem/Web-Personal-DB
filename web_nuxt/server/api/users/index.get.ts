import { drizzle } from "db0/integrations/drizzle";
import { like } from "drizzle-orm";
import { db } from "~/server/db/index";
import { usersTable } from "~/server/db/src/schema";

export default defineEventHandler(async (event) => {
  const search = getQuery(event).search as string;
  const drizzleDb = drizzle(db);
  if (search && search.length > 2) {
    if (search.match(/^[a-zA-Z_]+$/)) {
      const query = drizzleDb
        .select()
        .from(usersTable)
        .where(like(usersTable.username, `%${search}%`));
      const results = await query.all();
      return { search: results };
    } else {
      const query = drizzleDb
        .select()
        .from(usersTable)
        .where(like(usersTable.fullname, `%${search}%`));
      const results = await query.all();
      return { search: results };
    }
  }
  const query = drizzleDb.select().from(usersTable);
  const results = await query.all();
  return { search: results };
});
