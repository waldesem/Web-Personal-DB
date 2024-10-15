import { db } from "~/server/db/index";

export default defineEventHandler(async(event) => {
  const item = getRouterParam(event, 'item')
  const item_id = getRouterParam(event, 'item_id')
  await db.sql`DELETE FROM {${item}} WHERE id = ${item_id}`
  return { message: "success" }
})