export default defineEventHandler(async () => {
  const db = useDatabase();

  try {
    const stmt = db.prepare(`SELECT * FROM users WHERE`);
    return stmt.all();
  } catch (error) {
    console.error(error);
    return [];
  }
});
