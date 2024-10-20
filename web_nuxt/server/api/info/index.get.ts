import { and, count, gte, lte, eq } from "drizzle-orm";
import { db } from "~/server/db/index";
import { persons, checks } from "~/server/db/src/schema";
import { currentUser, Regions } from "~/server/utils";

export default defineEventHandler(async (event) => {
  const curUser = await currentUser(); // TODO: refactor
  const { region, start, end } = getQuery(event) as Record<string, string>;
  return await db
    .select({ conclusion: checks.conclusion, count: count() })
    .from(checks)
    .leftJoin(persons, eq(checks.person_id, persons.id))
    .where(
      and(
        gte(checks.created, start),
        lte(checks.created, end),
        eq(
          persons.region,
          region ? Regions[region as keyof typeof Regions] : curUser.region
        )
      )
    )
    .groupBy(checks.conclusion);
});
