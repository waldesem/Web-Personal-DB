import { drizzle } from "db0/integrations/drizzle";
import { db } from "~/server/db/index";
import { itemsTables } from "~/server/db/src/schema";

export default defineEventHandler(async (event) => {
  const item = getRouterParam(event, "item");
  const item_id = getRouterParam(event, "item_id");
  const data = await readBody(event);
  const table = itemsTables[item as keyof typeof itemsTables];
  const drizzleDb = drizzle(db);
  if (item !== "persons") {
    Object.assign(data, {
      person_id: item_id,
      user_id: "current_user",
    });
  }
  try {
    await drizzleDb.insert(table).values(data).onConflictDoUpdate({
      target: table.id,
      set: data,
    });
    return { message: "success" };
  } catch (error) {
    return { error: error };
  }
});
