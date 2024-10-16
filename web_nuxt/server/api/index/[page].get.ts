import { drizzle } from "db0/integrations/drizzle";
import { desc, like } from "drizzle-orm";
import { db } from "~/server/db/index";
import { persons } from "~/server/db/src/schema";

export default defineEventHandler(async (event) => {
  const pagination = 10;
  const page = parseInt(getRouterParam(event, "page") as string);
  const search = getQuery(event).search as string;
  const drizzleDb = drizzle(db);
  let query = drizzleDb.select().from(persons).$dynamic();
  if (search && search.length > 2) {
    const searchData = search.toUpperCase().split(" ").slice(0, 3);
    if (searchData.length) {
      query = query.where(like(persons.surname, `%${searchData[0]}%`));
    }
    if (searchData.length > 1) {
      query = query.where(like(persons.firstname, `%${searchData[1]}%`));
    }
    if (searchData.length > 2) {
      query = query.where(like(persons.patronymic, `%${searchData[2]}%`));
    }
  }
  // if current_user.get("region") != Regions.main.value:
  //     stmt = stmt.filter(Persons.region == current_user.get("region"))
  query = query
    .limit(pagination + 1)
    .offset((page - 1) * pagination)
    .orderBy(desc(persons.id));
  const results = await query.all();
  const hasNext = results.length > pagination;
  return [hasNext ? results.slice(0, pagination) : results, hasNext];
});
