import { SECRET_KEY } from "~~/server/utils";

export default defineEventHandler((event) => {
  clearSession(event, {
    password: SECRET_KEY,
  });
  return "";
});
