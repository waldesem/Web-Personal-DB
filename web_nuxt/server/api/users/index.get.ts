import { drizzle } from "drizzle-orm/better-sqlite3";
import { like } from "drizzle-orm";
import { db } from "~/server/db/index";
import { usersTable } from "~/server/db/src/schema";

export default defineEventHandler(async(event) => {
  const search = getQuery(event).search as string;
  const drizzleDb = drizzle(db);
  const results = await drizzleDb
    .select()
    .from(usersTable)
    .where(like(usersTable.username, `%${search}%`))
    // .all();
  return { search: results };
});
