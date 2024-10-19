import { db } from "~/server/db/index";
import { sql } from "drizzle-orm";

export default defineEventHandler(async (event) => {
  const item = getRouterParam(event, "item");
  const item_id = getRouterParam(event, "item_id");
  try {
    db.run(sql`DELETE FROM {${item}} WHERE id = ${item_id}`);
    return { message: "success" };
  } catch (error) {
    return { error: error };
  }
});
