import { db } from "~/server/db/index";

export default defineEventHandler(async (event) => {
  const item = getRouterParam(event, "item");
  const item_id = getRouterParam(event, "item_id");
  const { rows } =
    await db.sql`SELECT {${item}}.*, users.fullname as username FROM {${item}} \
    LEFT JOIN users ON users.id = {${item}}.user_id WHERE {${item}}.{${
      item == "persons" ? "id" : "person_id"
    }} = {${item_id}}`;
  return rows;
});
