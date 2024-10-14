import { integer, sqliteTable, text } from "drizzle-orm/sqlite-core";

export const usersTable = sqliteTable("users", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  fullname: text("fullname", { mode: "text" }).notNull(),
  username: text("username", { mode: "text" }).notNull().unique(),
  email: text("email", { mode: "text" }).notNull().unique(),
  passhash: text("passhash", { mode: "text" }).notNull(),
  pswd_create: integer("pswd_create", { mode: "timestamp_ms" }).notNull(),
  change_pswd: integer("change_pswd", { mode: "boolean" }).notNull(),
  blocked: integer("blocked", { mode: "boolean" }).notNull(),
  deleted: integer("deleted", { mode: "boolean" }).notNull(),
  attempt: integer("attempt", { mode: "number" }).notNull(),
  role: text("role", { mode: "text" }).notNull(),
  created: integer("created", { mode: "timestamp_ms" }).notNull(),
});

export const personsTable = sqliteTable("persons", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  surname: text("surname", { mode: "text" }).notNull(),
  firstname: text("firstname", { mode: "text" }).notNull(),
  patronymic: text("patronymic", { mode: "text" }),
  birthday: integer("birthday", { mode: "timestamp" }).notNull(),
  birthplace: text("birthplace", { mode: "text" }),
  citizenship: text("citizenship", { mode: "text" }),
  dual: text("dual", { mode: "text" }),
  snils: text("snils", { mode: "text" }),
  inn: text("inn", { mode: "text" }),
  marital: text("marital", { mode: "text" }),
  addition: text("addition", { mode: "text" }),
  destination: text("destination", { mode: "text" }),
  created: integer("created", { mode: "timestamp_ms" }).notNull(),
  region: text("region", { mode: "text" }),
  editable: integer("editable", { mode: "boolean" }).notNull().default(false),
  user_id: integer("user_id", { mode: "number" }).references(() => usersTable.id),
});

export const previousTable = sqliteTable("previous", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  surname: text("surname", { mode: "text" }).notNull(),
  firstname: text("firstname", { mode: "text" }).notNull(),
  patronymic: text("patronymic", { mode: "text" }),
  changed: text("changed", { mode: "text" }),
  reason: text("reason", { mode: "text" }),
  created: integer("created", { mode: "timestamp_ms" }).notNull(),
  person_id: integer("person_id", { mode: "number" }).references(
    () => personsTable.id
  ),
  user_id: integer("user_id", { mode: "number" }).references(
    () => usersTable.id
  ),
});

export const educationsTable = sqliteTable("educations", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  view: text("view", { mode: "text" }).notNull(),
  institution: text("institution", { mode: "text" }).notNull(),
  finished: text("finished", { mode: "text" }).notNull(),
  specialty: text("specialty", { mode: "text" }),
  created: integer("created", { mode: "timestamp_ms" }).notNull(),
  person_id: integer("person_id", { mode: "number" }).references(
    () => personsTable.id
  ),
  user_id: integer("user_id", { mode: "number" }).references(
    () => usersTable.id
  ),
});

export const staffsTable = sqliteTable("staffs", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  position: text("position", { mode: "text" }).notNull(),
  department: text("department", { mode: "text" }).notNull(),
  created: integer("created", { mode: "timestamp_ms" }).notNull(),
  person_id: integer("person_id", { mode: "number" }).references(
    () => personsTable.id
  ),
  user_id: integer("user_id", { mode: "number" }).references(
    () => usersTable.id
  ),
});

export const addressesTable = sqliteTable("documents", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  view: text("view", { mode: "text" }).notNull(),
  series: text("series", { mode: "text" }),
  digits: text("digits", { mode: "text" }),
  agency: text("agency", { mode: "text" }),
  issue: integer("issue", { mode: "timestamp" }),
  created: integer("created", { mode: "timestamp_ms" }).notNull(),
  person_id: integer("person_id", { mode: "number" }).references(
    () => personsTable.id
  ),
  user_id: integer("user_id", { mode: "number" }).references(
    () => usersTable.id
  ),
});

export const contactsTable = sqliteTable("addresses", {
  id: integer("number").primaryKey({ autoIncrement: true }),
  view: text("text"),
  addresses: text("text"),
  created: integer("timestamp_ms").notNull(),
  person_id: integer("number").references(() => personsTable.id),
  user_id: integer("number").references(() => usersTable.id),
});

export const documentsTable = sqliteTable("contacts", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  view: text("view", { mode: "text" }).notNull(),
  created: integer("created", { mode: "timestamp_ms" }).notNull(),
  person_id: integer("person_id", { mode: "number" }).references(
    () => personsTable.id
  ),
  user_id: integer("user_id", { mode: "number" }).references(
    () => usersTable.id
  ),
});

export const workplacesTable = sqliteTable("workplaces", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  now_work: integer("now_work", { mode: "boolean" }).notNull().default(false),
  starts: integer("starts", { mode: "timestamp" }).notNull(),
  finished: integer("finished", { mode: "timestamp" }),
  workplace: text("workplace", { mode: "text" }).notNull(),
  addresses: text("addresses", { mode: "text" }),
  position: text("position", { mode: "text" }),
  reason: text("reason", { mode: "text" }),
  created: integer("created", { mode: "timestamp_ms" }).notNull(),
  person_id: integer("person_id", { mode: "number" }).references(
    () => personsTable.id
  ),
  user_id: integer("user_id", { mode: "number" }).references(
    () => usersTable.id
  ),
});

export const affilationsTable = sqliteTable("affilations", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  view: text("view", { mode: "text" }).notNull(),
  organization: text("organization", { mode: "text" }).notNull(),
  inn: text("inn", { mode: "text" }),
  created: integer("created", { mode: "timestamp_ms" }).notNull(),
  person_id: integer("person_id", { mode: "number" }).references(
    () => personsTable.id
  ),
  user_id: integer("user_id", { mode: "number" }).references(
    () => usersTable.id
  ),
});

export const relationsTable = sqliteTable("relations", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  relation: text("relation", { mode: "text" }).notNull(),
  relation_id: integer("relation_id", { mode: "number" }).notNull(),
  created: integer("created", { mode: "timestamp_ms" }).notNull(),
  person_id: integer("person_id", { mode: "number" }).references(
    () => personsTable.id
  ),
  user_id: integer("user_id", { mode: "number" }).references(
    () => usersTable.id
  ),
});

export const checksTable = sqliteTable("checks", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  workplace: text("workplace", { mode: "text" }),
  document: text("document", { mode: "text" }),
  inn: text("inn", { mode: "text" }),
  debt: text("debt", { mode: "text" }),
  bankruptcy: text("bankruptcy", { mode: "text" }),
  bki: text("bki", { mode: "text" }),
  courts: text("courts", { mode: "text" }),
  affilation: text("affilation", { mode: "text" }),
  terrorist: text("terrorist", { mode: "text" }),
  mvd: text("mvd", { mode: "text" }),
  internet: text("internet", { mode: "text" }),
  cronos: text("cronos", { mode: "text" }),
  cros: text("cros", { mode: "text" }),
  addition: text("addition", { mode: "text" }),
  comment: text("comment", { mode: "text" }),
  conclusion: text("conclusion", { mode: "text" }),
  created: integer("created", { mode: "timestamp_ms" }).notNull(),
  person_id: integer("person_id", { mode: "number" }).references(
    () => personsTable.id
  ),
  user_id: integer("user_id", { mode: "number" }).references(
    () => usersTable.id
  ),
});

export const poligrafsTable = sqliteTable("poligrafs", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  theme: text("theme", { mode: "text" }),
  results: text("results", { mode: "text" }),
  created: integer("created", { mode: "timestamp_ms" }).notNull(),
  person_id: integer("person_id", { mode: "number" }).references(
    () => personsTable.id
  ),
  user_id: integer("user_id", { mode: "number" }).references(
    () => usersTable.id
  ),
});

export const investigationsTable = sqliteTable("investigations", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  theme: text("theme", { mode: "text" }),
  info: text("info", { mode: "text" }),
  created: integer("created", { mode: "timestamp_ms" }).notNull(),
  person_id: integer("person_id", { mode: "number" }).references(
    () => personsTable.id
  ),
  user_id: integer("user_id", { mode: "number" }).references(
    () => usersTable.id
  ),
});

export const inquiriesTable = sqliteTable("inquiries", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  info: text("info", { mode: "text" }),
  initiator: text("initiator", { mode: "text" }),
  origins: text("origins", { mode: "text" }),
  created: integer("created", { mode: "timestamp_ms" }).notNull(),
  person_id: integer("person_id", { mode: "number" }).references(
    () => personsTable.id
  ),
  user_id: integer("user_id", { mode: "number" }).references(
    () => usersTable.id
  ),
});
