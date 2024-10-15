import { db } from "~/server/db/index";

export default defineEventHandler(async (event) => {
  const item_id = getRouterParam(event, "item_id");
  const editables = (
    await db.sql`SELECT editable FROM persons WHERE id = ${item_id}`
  ).rows as Array<Record<string, boolean>>;
  if (editables.length == 0) {
    return { message: "error" };
  }
  const firstRow = editables[0];
  const editable = firstRow["editable" as keyof typeof firstRow] ? 0 : 1;
  await db.sql`UPDATE persons SET editable = ${editable} WHERE id = ${item_id}`;
  return { message: "success" };
});
