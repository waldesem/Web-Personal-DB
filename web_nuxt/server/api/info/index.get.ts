import { and, count, gte, lte, eq } from "drizzle-orm";
import { db } from "~/server/db/index";
import { persons, checks } from "~/server/db/src/schema";

export default defineEventHandler(async (event) => {
  const region = getQuery(event).region as string;
  const start = getQuery(event).start as string;
  const end = getQuery(event).end as string;
  const results = await db
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
  return results;
});
