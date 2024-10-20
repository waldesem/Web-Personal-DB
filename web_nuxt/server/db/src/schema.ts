import { z } from "zod";
import { index, integer, sqliteTable, text } from "drizzle-orm/sqlite-core";
import { createInsertSchema } from "drizzle-zod";
import { sql } from "drizzle-orm";

export const users = sqliteTable("users", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  fullname: text("fullname", { mode: "text" }).notNull(),
  username: text("username", { mode: "text" }).notNull().unique(),
  email: text("email", { mode: "text" }).notNull().unique(),
  passhash: text("passhash", { mode: "text" }).notNull().$default(
    () => createPasswordHash("88888888")
  ),
  pswd_create: text("pswd_create", { mode: "text" }).notNull().$default(
    () => sql`(CURRENT_TIMESTAMP)`
  ),
  change_pswd: integer("change_pswd", { mode: "boolean" }).notNull().default(true),
  blocked: integer("blocked", { mode: "boolean" }).notNull().default(false),
  deleted: integer("deleted", { mode: "boolean" }).notNull().default(false),
  attempt: integer("attempt", { mode: "number" }).notNull().default(0),
  role: text("role", { mode: "text" }).notNull().default("guest"),
  region: text("region", { mode: "text" }).notNull().default("Главный офис"),
  created: text("created", { mode: "text" }).notNull().default(sql`(CURRENT_TIMESTAMP)`),
});

export const userSchema = createInsertSchema(users);

export const persons = sqliteTable(
  "persons",
  {
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
    created: text("created", { mode: "text" }).default(
      sql`(CURRENT_TIMESTAMP)`
    ),
    region: text("region", { mode: "text" }),
    editable: integer("editable", { mode: "boolean" }).default(false),
    user_id: integer("user_id", { mode: "number" }).references(() => users.id),
  },
  (table) => {
    return {
      surnameIdx: index("surname_idx").on(table.surname),
      firstnameIdx: index("firstname_idx").on(table.firstname),
      patronymicIdx: index("patronymic_idx").on(table.patronymic),
    };
  }
);

export const personSchema = createInsertSchema(persons).extend({
  username: z.string(),
});

export const previous = sqliteTable("previous", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  surname: text("surname", { mode: "text" }).notNull(),
  firstname: text("firstname", { mode: "text" }).notNull(),
  patronymic: text("patronymic", { mode: "text" }),
  changed: text("changed", { mode: "text" }),
  reason: text("reason", { mode: "text" }),
  created: text("created", { mode: "text" }).default(sql`(CURRENT_TIMESTAMP)`),
  person_id: integer("person_id", { mode: "number" }).references(
    () => persons.id
  ),
  user_id: integer("user_id", { mode: "number" }).references(() => users.id),
});

export const educations = sqliteTable("educations", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  view: text("view", { mode: "text" }).notNull(),
  institution: text("institution", { mode: "text" }).notNull(),
  finished: text("finished", { mode: "text" }).notNull(),
  specialty: text("specialty", { mode: "text" }),
  created: text("created", { mode: "text" }).default(sql`(CURRENT_TIMESTAMP)`),
  person_id: integer("person_id", { mode: "number" }).references(
    () => persons.id
  ),
  user_id: integer("user_id", { mode: "number" }).references(() => users.id),
});

export const staffs = sqliteTable("staffs", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  position: text("position", { mode: "text" }).notNull(),
  department: text("department", { mode: "text" }).notNull(),
  created: text("created", { mode: "text" }).default(sql`(CURRENT_TIMESTAMP)`),
  person_id: integer("person_id", { mode: "number" }).references(
    () => persons.id
  ),
  user_id: integer("user_id", { mode: "number" }).references(() => users.id),
});

export const addresses = sqliteTable("documents", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  view: text("view", { mode: "text" }).notNull(),
  series: text("series", { mode: "text" }),
  digits: text("digits", { mode: "text" }),
  agency: text("agency", { mode: "text" }),
  issue: integer("issue", { mode: "timestamp" }),
  created: text("created", { mode: "text" }).default(sql`(CURRENT_TIMESTAMP)`),
  person_id: integer("person_id", { mode: "number" }).references(
    () => persons.id
  ),
  user_id: integer("user_id", { mode: "number" }).references(() => users.id),
});

export const contacts = sqliteTable("addresses", {
  id: integer("number").primaryKey({ autoIncrement: true }),
  view: text("text"),
  addresses: text("text"),
  created: text("created", { mode: "text" }).default(sql`(CURRENT_TIMESTAMP)`),
  person_id: integer("number").references(() => persons.id),
  user_id: integer("number").references(() => users.id),
});

export const documents = sqliteTable("contacts", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  view: text("view", { mode: "text" }).notNull(),
  created: text("created", { mode: "text" }).default(sql`(CURRENT_TIMESTAMP)`),
  person_id: integer("person_id", { mode: "number" }).references(
    () => persons.id
  ),
  user_id: integer("user_id", { mode: "number" }).references(() => users.id),
});
export const workplaces = sqliteTable("workplaces", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  now_work: integer("now_work", { mode: "boolean" }).default(false),
  starts: integer("starts", { mode: "timestamp" }).notNull(),
  finished: integer("finished", { mode: "timestamp" }),
  workplace: text("workplace", { mode: "text" }).notNull(),
  addresses: text("addresses", { mode: "text" }),
  position: text("position", { mode: "text" }),
  reason: text("reason", { mode: "text" }),
  created: text("created", { mode: "text" }).default(sql`(CURRENT_TIMESTAMP)`),
  person_id: integer("person_id", { mode: "number" }).references(
    () => persons.id
  ),
  user_id: integer("user_id", { mode: "number" }).references(() => users.id),
});

export const affilations = sqliteTable("affilations", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  view: text("view", { mode: "text" }).notNull(),
  organization: text("organization", { mode: "text" }).notNull(),
  inn: text("inn", { mode: "text" }),
  created: text("created", { mode: "text" }).default(sql`(CURRENT_TIMESTAMP)`),
  person_id: integer("person_id", { mode: "number" }).references(
    () => persons.id
  ),
  user_id: integer("user_id", { mode: "number" }).references(() => users.id),
});

export const relations = sqliteTable("relations", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  relation: text("relation", { mode: "text" }).notNull(),
  relation_id: integer("relation_id", { mode: "number" }).notNull(),
  created: text("created", { mode: "text" }).default(sql`(CURRENT_TIMESTAMP)`),
  person_id: integer("person_id", { mode: "number" }).references(
    () => persons.id
  ),
  user_id: integer("user_id", { mode: "number" }).references(() => users.id),
});

export const checks = sqliteTable("checks", {
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
  created: text("created", { mode: "text" }).default(sql`(CURRENT_TIMESTAMP)`),
  person_id: integer("person_id", { mode: "number" }).references(
    () => persons.id
  ),
  user_id: integer("user_id", { mode: "number" }).references(() => users.id),
});

export const poligrafs = sqliteTable("poligrafs", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  theme: text("theme", { mode: "text" }),
  results: text("results", { mode: "text" }),
  created: text("created", { mode: "text" }).default(sql`(CURRENT_TIMESTAMP)`),
  person_id: integer("person_id", { mode: "number" }).references(
    () => persons.id
  ),
  user_id: integer("user_id", { mode: "number" }).references(() => users.id),
});

export const investigations = sqliteTable("investigations", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  theme: text("theme", { mode: "text" }),
  info: text("info", { mode: "text" }),
  created: text("created", { mode: "text" }).default(sql`(CURRENT_TIMESTAMP)`),
  person_id: integer("person_id", { mode: "number" }).references(
    () => persons.id
  ),
  user_id: integer("user_id", { mode: "number" }).references(() => users.id),
});

export const inquiries = sqliteTable("inquiries", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  info: text("info", { mode: "text" }),
  initiator: text("initiator", { mode: "text" }),
  origins: text("origins", { mode: "text" }),
  created: text("created", { mode: "text" }).default(sql`(CURRENT_TIMESTAMP)`),
  person_id: integer("person_id", { mode: "number" }).references(
    () => persons.id
  ),
  user_id: integer("user_id", { mode: "number" }).references(() => users.id),
});

export const itemsTables = {
  persons: persons,
  previous: previous,
  educations: educations,
  staffs: staffs,
  addresses: addresses,
  contacts: contacts,
  documents: documents,
  workplaces: workplaces,
  affilations: affilations,
  relations: relations,
  checks: checks,
  poligrafs: poligrafs,
  investigations: investigations,
  inquiries: inquiries,
};

export const itemsSchemas = {
  persons: personSchema,
  previous: createInsertSchema(previous),
  educations: createInsertSchema(educations),
  staffs: createInsertSchema(staffs),
  addresses: createInsertSchema(addresses),
  contacts: createInsertSchema(contacts),
  documents: createInsertSchema(documents),
  workplaces: createInsertSchema(workplaces),
  affilations: createInsertSchema(affilations),
  relations: createInsertSchema(relations),
  checks: createInsertSchema(checks),
  poligrafs: createInsertSchema(poligrafs),
  investigations: createInsertSchema(investigations),
  inquiries: createInsertSchema(inquiries),
};
