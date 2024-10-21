import { sql } from "drizzle-orm";
import { db } from "~/server/db/index";
import { itemsTables } from "~/server/db/src/schema";

export default defineEventHandler(async (event) => {
  const item = getRouterParam(event, "item");
  const item_id = getRouterParam(event, "item_id");
  if (item == "persons") {
    for (const item in Object.keys(itemsTables)) {
      if (item == "persons") continue;
      db.run(sql`DELETE FROM {${item}} WHERE person_id = ${item_id}`);
    }
    db.run(sql`DELETE FROM persons WHERE id = ${item_id}`);
    return { message: "success" };
  }
  db.run(sql`DELETE FROM {${item}} WHERE id = ${item_id}`);
  return { message: "success" };
});
