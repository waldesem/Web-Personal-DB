import { drizzle } from "db0/integrations/drizzle";
import { db } from "~/server/db/index";
import { itemsTables, itemsSchemas } from "~/server/db/src/schema";

export default defineEventHandler(async (event) => {
  const item = getRouterParam(event, "item");
  const item_id = getRouterParam(event, "item_id");
  const data = await readBody(event);
  const schema = itemsSchemas[item as keyof typeof itemsSchemas];
  const table = itemsTables[item as keyof typeof itemsTables];
  const validated = schema.parse(data);
  const drizzleDb = drizzle(db);
  Object.assign(validated, { user_id: "current_user" });
  if (item !== "persons") {
    Object.assign(validated, { person_id: item_id });
  } else {
    Object.assign(validated, { id: item_id });
  }
  try {
    await drizzleDb.insert(table).values(validated).onConflictDoUpdate({
      target: table.id,
      set: validated,
    });
    return { message: "success" };
  } catch (error) {
    return { error: error };
  }
});
