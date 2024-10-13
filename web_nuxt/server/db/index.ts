import { createDatabase } from "db0";
import sqlite from "db0/connectors/better-sqlite3";

export const db = createDatabase(
  sqlite({
    path: process.env.DATABASE_URL,
  })
);
