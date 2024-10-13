import { integer, sqliteTable, text } from "drizzle-orm/sqlite-core";

export const usersTable = sqliteTable("users", {
  id: integer('id', { mode: 'number' }).primaryKey({ autoIncrement: true }),
  fullname: text('fullname', { mode: 'text' }).notNull(),
  username: text('username', { mode: 'text' }).notNull().unique(),
  email: text('email', { mode: 'text' }).notNull().unique(),
  passhash: text('passhash', { mode: 'text' }).notNull(),
  pswd_create: integer('pswd_create', { mode: 'timestamp_ms' }).notNull(),
  change_pswd: integer('change_pswd', { mode: 'boolean' }).notNull(),
  blocked: integer('blocked', { mode: 'boolean' }).notNull(),
  deleted: integer('deleted', { mode: 'boolean' }).notNull(),
  attempt: integer('attempt', { mode: 'number' }).notNull(),
  role: text('role', { mode: 'text' }).notNull(),
  created: integer('created', { mode: 'timestamp_ms' }).notNull(),
});

export const personsTable = sqliteTable("persons", {
  id: integer('number').primaryKey({ autoIncrement: true }),
  surname: text('text').notNull(),
  firstname: text('text').notNull(),
  patronymic: text('text'),
  birthday: integer('timestamp').notNull(),
  birthplace: text('text'),
  citizenship: text('text'),
  dual: text('text'),
  snils: text('text'),
  inn: text('text'),
  marital: text('text'),
  addition: text('text'),
  destination: text('text'),
  created: integer('timestamp_ms').notNull(),
  region: text('text'),
  editable: integer('boolean').notNull(),
  user_id: integer('number').references(() => usersTable.id),
})

export const previousTable = sqliteTable("previous", {
  id: integer('number').primaryKey({ autoIncrement: true }),
  surname: text('text'),
  firstname: text('text'),
  patronymic: text('text'),
  changed: text('text'),
  reason: text('text'),
  created: integer('timestamp_ms').notNull(),
  person_id: integer('number').references(() => personsTable.id),
  user_id: integer('number').references(() => usersTable.id),
})

export const educationsTable = sqliteTable("educations", {
  id: integer('number').primaryKey({ autoIncrement: true }),
  view: text('text'),
  institution: text('text'),
  finished: integer('number'),
  specialty: text('text'),
  created: integer('timestamp_ms').notNull(),
  person_id: integer('number').references(() => personsTable.id),
  user_id: integer('number').references(() => usersTable.id),
})

export const staffsTable = sqliteTable("staffs", {
  id: integer('number').primaryKey({ autoIncrement: true }),
  position: text('text'),
  department: text('text'),
  created: integer('timestamp_ms').notNull(),
  person_id: integer('number').references(() => personsTable.id),
  user_id: integer('number').references(() => usersTable.id),
})

export const addressesTable = sqliteTable("documents", {
  id: integer('number').primaryKey({ autoIncrement: true }),
  view: text('text'),
  series: text('text'),
  digits: text('text'),
  agency: text('text'),
  issue: integer('timestamp'),
  created: integer('timestamp_ms').notNull(),
  person_id: integer('number').references(() => personsTable.id),
  user_id: integer('number').references(() => usersTable.id),
})

export const contactsTable = sqliteTable("addresses", {
  id: integer('number').primaryKey({ autoIncrement: true }),
  view: text('text'),
  addresses: text('text'),
  created: integer('timestamp_ms').notNull(),
  person_id: integer('number').references(() => personsTable.id),
  user_id: integer('number').references(() => usersTable.id),
})

export const documentsTable = sqliteTable("contacts", {
  id: integer('number').primaryKey({ autoIncrement: true }),
  view: text('text'),
  created: integer('timestamp_ms').notNull(),
  person_id: integer('number').references(() => personsTable.id),
  user_id: integer('number').references(() => usersTable.id),
})

export const workplacesTable = sqliteTable("workplaces", {
  id: integer('number').primaryKey({ autoIncrement: true }),
  now_work: integer('boolean'),
  starts: integer('timestamp'),
  finished: integer('timestamp'),
  workplace: text('text'),
  addresses: text('text'),
  position: text('text'),
  reason: text('text'),
  created: integer('timestamp_ms').notNull(),
  person_id: integer('number').references(() => personsTable.id),
  user_id: integer('number').references(() => usersTable.id),
})

export const affilationsTable = sqliteTable("affilations", {
  id: integer('number').primaryKey({ autoIncrement: true }),
  view: text('text'),
  organization: text('text'),
  inn: text('text'),
  created: integer('timestamp_ms').notNull(),
  person_id: integer('number').references(() => personsTable.id),
  user_id: integer('number').references(() => usersTable.id),
})

export const relationsTable = sqliteTable("relations", {
  id: integer('number').primaryKey({ autoIncrement: true }),
  relation: text('text'),
  relation_id: integer('number'),
  created: integer('timestamp_ms').notNull(),
  person_id: integer('number').references(() => personsTable.id),
  user_id: integer('number').references(() => usersTable.id),
})

export const checksTable = sqliteTable("checks", {
  id: integer('number').primaryKey({ autoIncrement: true }),
  workplace: text('text'),
  document: text('text'),
  inn: text('text'),
  debt: text('text'),
  bankruptcy: text('text'),
  bki: text('text'),
  courts: text('text'),
  affilation: text('text'),
  terrorist: text('text'),
  mvd: text('text'),
  internet: text('text'),
  cronos: text('text'),
  cros: text('text'),
  addition: text('text'),
  comment: text('text'),
  conclusion: text('text'),
  created: integer('timestamp_ms').notNull(),
  person_id: integer('number').references(() => personsTable.id),
  user_id: integer('number').references(() => usersTable.id),
})

export const poligrafsTable = sqliteTable("poligrafs", {
  id: integer('number').primaryKey({ autoIncrement: true }),
  theme: text('text'),
  results: text('text'),
  created: integer('timestamp_ms').notNull(),
  person_id: integer('number').references(() => personsTable.id),
  user_id: integer('number').references(() => usersTable.id),
})

export const investigationsTable = sqliteTable("investigations", {
  id: integer('number').primaryKey({ autoIncrement: true }),
  theme: text('text'),
  info: text('text'),
  created: integer('timestamp_ms').notNull(),
  person_id: integer('number').references(() => personsTable.id),
  user_id: integer('number').references(() => usersTable.id),
})

export const inquiriesTable = sqliteTable("inquiries", {
  id: integer('number').primaryKey({ autoIncrement: true }),
  info: text('text'),
  initiator: text('text'),
  origins: text('text'),
  created: integer('timestamp_ms').notNull(),
  person_id: integer('number').references(() => personsTable.id),
  user_id: integer('number').references(() => usersTable.id),
})
