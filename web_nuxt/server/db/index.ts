import { drizzle } from 'drizzle-orm/better-sqlite3';

export function getDb() {
  return db;
}

const db = drizzle( process.env.DATABASE_URL);