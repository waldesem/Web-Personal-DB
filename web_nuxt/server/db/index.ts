import { createDatabase } from "db0";
import sqlite from "db0/connectors/better-sqlite3";

export const db = createDatabase(
  sqlite({
    path: process.env.DATABASE_URL,
  })
);

// import { drizzle } from 'drizzle-orm/better-sqlite3';
// import Database from 'better-sqlite3';

// export const db = drizzle(new Database(process.env.DATABASE_URL));