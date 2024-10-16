import { drizzle } from "db0/integrations/drizzle";
import { and, count, gte, lte, eq } from "drizzle-orm";
import { db } from "~/server/db/index";
import { persons, checks } from "~/server/db/src/schema";

export default defineEventHandler(async (event) => {
  const region = getQuery(event).region as string;
  const start = getQuery(event).start as Date;
  const end = getQuery(event).end as Date;
  const drizzleDb = drizzle(db);
  const query = drizzleDb
    .select({ value: count() })
    .from(checks)
    .leftJoin(persons, eq(checks.person_id, persons.id))
    .where(
      and(
        gte(checks.created, start),
        lte(checks.created, end),
        eq(persons.region, region ? region : "current_user.region")
      )
    )
    .groupBy(checks.conclusion);
  const results = await query.all();
  return results;
});
