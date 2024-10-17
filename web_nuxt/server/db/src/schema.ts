import { z } from "zod";
import { index, integer, sqliteTable, text } from "drizzle-orm/sqlite-core";
import { createInsertSchema, createSelectSchema } from "drizzle-zod";

export const users = sqliteTable("users", {
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

export const insertUserSchema = createInsertSchema(users);
export const selectUserSchema = createSelectSchema(users);

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
    created: integer("created", { mode: "timestamp_ms" }).notNull(),
    region: text("region", { mode: "text" }),
    editable: integer("editable", { mode: "boolean" }).notNull().default(false),
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

export const insertPersonSchema = createInsertSchema(persons).extend({
  username: z.string(),
});
export const selectPersonSchema = createSelectSchema(persons);

export const previous = sqliteTable("previous", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  surname: text("surname", { mode: "text" }).notNull(),
  firstname: text("firstname", { mode: "text" }).notNull(),
  patronymic: text("patronymic", { mode: "text" }),
  changed: text("changed", { mode: "text" }),
  reason: text("reason", { mode: "text" }),
  created: integer("created", { mode: "timestamp_ms" }).notNull(),
  person_id: integer("person_id", { mode: "number" }).references(
    () => persons.id
  ),
  user_id: integer("user_id", { mode: "number" }).references(() => users.id),
});

export const insertPreviousSchema = createInsertSchema(previous);
export const selectPreviousSchema = createSelectSchema(previous);

export const educations = sqliteTable("educations", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  view: text("view", { mode: "text" }).notNull(),
  institution: text("institution", { mode: "text" }).notNull(),
  finished: text("finished", { mode: "text" }).notNull(),
  specialty: text("specialty", { mode: "text" }),
  created: integer("created", { mode: "timestamp_ms" }).notNull(),
  person_id: integer("person_id", { mode: "number" }).references(
    () => persons.id
  ),
  user_id: integer("user_id", { mode: "number" }).references(() => users.id),
});

export const insertEducationSchema = createInsertSchema(educations);
export const selectEducationSchema = createSelectSchema(educations);

export const staffs = sqliteTable("staffs", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  position: text("position", { mode: "text" }).notNull(),
  department: text("department", { mode: "text" }).notNull(),
  created: integer("created", { mode: "timestamp_ms" }).notNull(),
  person_id: integer("person_id", { mode: "number" }).references(
    () => persons.id
  ),
  user_id: integer("user_id", { mode: "number" }).references(() => users.id),
});

export const insertStaffSchema = createInsertSchema(staffs);
export const selectStaffSchema = createSelectSchema(staffs);

export const addresses = sqliteTable("documents", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  view: text("view", { mode: "text" }).notNull(),
  series: text("series", { mode: "text" }),
  digits: text("digits", { mode: "text" }),
  agency: text("agency", { mode: "text" }),
  issue: integer("issue", { mode: "timestamp" }),
  created: integer("created", { mode: "timestamp_ms" }).notNull(),
  person_id: integer("person_id", { mode: "number" }).references(
    () => persons.id
  ),
  user_id: integer("user_id", { mode: "number" }).references(() => users.id),
});

export const insertAddressSchema = createInsertSchema(addresses);
export const selectAddressSchema = createSelectSchema(addresses);

export const contacts = sqliteTable("addresses", {
  id: integer("number").primaryKey({ autoIncrement: true }),
  view: text("text"),
  addresses: text("text"),
  created: integer("timestamp_ms").notNull(),
  person_id: integer("number").references(() => persons.id),
  user_id: integer("number").references(() => users.id),
});

export const insertContactSchema = createInsertSchema(contacts);
export const selectContactSchema = createSelectSchema(contacts);

export const documents = sqliteTable("contacts", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  view: text("view", { mode: "text" }).notNull(),
  created: integer("created", { mode: "timestamp_ms" }).notNull(),
  person_id: integer("person_id", { mode: "number" }).references(
    () => persons.id
  ),
  user_id: integer("user_id", { mode: "number" }).references(() => users.id),
});

export const insertDocumentSchema = createInsertSchema(documents);
export const selectDocumentSchema = createSelectSchema(documents);

export const workplaces = sqliteTable("workplaces", {
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
    () => persons.id
  ),
  user_id: integer("user_id", { mode: "number" }).references(() => users.id),
});

export const insertWorkplaceSchema = createInsertSchema(workplaces);
export const selectWorkplaceSchema = createSelectSchema(workplaces);

export const affilations = sqliteTable("affilations", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  view: text("view", { mode: "text" }).notNull(),
  organization: text("organization", { mode: "text" }).notNull(),
  inn: text("inn", { mode: "text" }),
  created: integer("created", { mode: "timestamp_ms" }).notNull(),
  person_id: integer("person_id", { mode: "number" }).references(
    () => persons.id
  ),
  user_id: integer("user_id", { mode: "number" }).references(() => users.id),
});

export const insertAffilationsSchema = createInsertSchema(affilations);
export const selectAffilationsSchema = createSelectSchema(affilations);

export const relations = sqliteTable("relations", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  relation: text("relation", { mode: "text" }).notNull(),
  relation_id: integer("relation_id", { mode: "number" }).notNull(),
  created: integer("created", { mode: "timestamp_ms" }).notNull(),
  person_id: integer("person_id", { mode: "number" }).references(
    () => persons.id
  ),
  user_id: integer("user_id", { mode: "number" }).references(() => users.id),
});

export const insertRelationSchema = createInsertSchema(relations);
export const selectRelationSchema = createSelectSchema(relations);

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
  created: integer("created", { mode: "timestamp_ms" }).notNull(),
  person_id: integer("person_id", { mode: "number" }).references(
    () => persons.id
  ),
  user_id: integer("user_id", { mode: "number" }).references(() => users.id),
});

export const insertCheckSchema = createInsertSchema(checks);
export const selectCheckSchema = createSelectSchema(checks);

export const poligrafs = sqliteTable("poligrafs", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  theme: text("theme", { mode: "text" }),
  results: text("results", { mode: "text" }),
  created: integer("created", { mode: "timestamp_ms" }).notNull(),
  person_id: integer("person_id", { mode: "number" }).references(
    () => persons.id
  ),
  user_id: integer("user_id", { mode: "number" }).references(() => users.id),
});

export const insertPoligrafSchema = createInsertSchema(poligrafs);
export const selectPoligrafSchema = createSelectSchema(poligrafs);

export const investigations = sqliteTable("investigations", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  theme: text("theme", { mode: "text" }),
  info: text("info", { mode: "text" }),
  created: integer("created", { mode: "timestamp_ms" }).notNull(),
  person_id: integer("person_id", { mode: "number" }).references(
    () => persons.id
  ),
  user_id: integer("user_id", { mode: "number" }).references(() => users.id),
});

export const insertInvestigationSchema = createInsertSchema(investigations);
export const selectInvestigationSchema = createSelectSchema(investigations);

export const inquiries = sqliteTable("inquiries", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  info: text("info", { mode: "text" }),
  initiator: text("initiator", { mode: "text" }),
  origins: text("origins", { mode: "text" }),
  created: integer("created", { mode: "timestamp_ms" }).notNull(),
  person_id: integer("person_id", { mode: "number" }).references(
    () => persons.id
  ),
  user_id: integer("user_id", { mode: "number" }).references(() => users.id),
});

export const insertInquirySchema = createInsertSchema(inquiries);
export const selectInquirySchema = createSelectSchema(inquiries);

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

export const itemsInsertModels = {
  persons: insertPersonSchema,
  previous: insertPreviousSchema,
  educations: insertEducationSchema,
  staffs: insertStaffSchema,
  addresses: insertAddressSchema,
  contacts: insertContactSchema,
  documents: insertDocumentSchema,
  workplaces: insertWorkplaceSchema,
  affilations: insertAffilationsSchema,
  relations: insertRelationSchema,
  checks: insertCheckSchema,
  poligrafs: insertPoligrafSchema,
  investigations: insertInvestigationSchema,
  inquiries: insertInquirySchema,
};

export const  anketaSchemaJson = z.object({
  lastName: z.string().max(255),
  firstName: z.string().max(255),
  midName: z.string().max(255).optional(),
  birthday: z.date(),
  birthplace: z.string(),
  citizen: z.string().optional(),
  additionalCitizenship: z.string().optional(),
  maritalStatus: z.string().optional(),
  inn: z.string().optional(),
  snils: z.string().optional(),
  positionName: z.string().optional(),
  department: z.string().optional(),
  passportSerial: z.string().optional(),
  passportNumber: z.string().optional(),
  passportIssueDate: z.string().optional(),
  passportIssuedBy: z.string().optional(),
  validAddress: z.string().optional(),
  regAddress: z.string().optional(),
  email: z.string().optional(),
  contactPhone: z.string().optional(),
})



  // educations: Optional[list[EducationJson]] = Field(
  //     alias="education",
  //     default=[],
  // )
  // workplaces: Optional[list[ExperienceJson]] = Field(
  //     alias="experience",
  //     default=[],
  // )
  // previous: Optional[list[NameWasChangedJson]] = Field(
  //     alias="nameWasChanged", default=[]
  // )
  // organizations: Optional[list[OrganizationsJson]] = []
  // relatedPersonsOrganizations: Optional[list[RelatedPersonsOrganizationsJson]] = []
  // stateOrganizations: Optional[list[StateOrganizationsJson]] = []
  // publicOfficeOrganizations: Optional[list[PublicOfficeOrganizationsJson]] = []

// export const nameWasChangedJson = z.object({
//   firstname: z.string().max(255).transform((value, ctx) => {
//     ctx.path = ["firstNameBeforeChange"];
//     return value.toUpperCase();
//   }).optional(),
// });

//     Optional[str] = Field(
//         alias="firstNameBeforeChange", default=None, max_length=255
//     )
//     surname: Optional[str] = Field(
//         alias="lastNameBeforeChange", default=None, max_length=255
//     )
//     patronymic: Optional[str] = Field(
//         alias="midNameBeforeChange", default=None, max_length=255
//     )
//     changed: Union[str, int] = Field(alias="yearOfChange", default=None)
//     reason: Optional[str] = None

// class EducationJson(BaseModel):
//     view: Optional[str] = Field(alias="educationType", default=None, max_length=255)
//     institution: Optional[str] = Field(alias="institutionName", default=None)
//     finished: Union[str, int] = Field(alias="endYear", default=None)
//     specialty: Optional[str] = None

// class ExperienceJson(BaseModel):
//     starts: Optional[date] = Field(alias="beginDate", default=None)
//     finished: Optional[date] = Field(alias="endDate", default=None)
//     now_work: Optional[bool] = Field(alias="currentJob", default=False)
//     workplace: Optional[str] = Field(alias="name", default=None, max_length=255)
//     addresses: Optional[str] = Field(alias="address", default=None, max_length=255)
//     position: Optional[str] = None
//     reason: Optional[str] = Field(alias="fireReason", default=None)

// class OrganizationsJson(BaseModel):
//     view: str = "Участвует в деятельности коммерческих организаций"
//     organization: Optional[str] = Field(alias="name", default=None)
//     inn: Optional[str] = None

// class RelatedPersonsOrganizationsJson(BaseModel):
//     view: str = "Связанные лица работают в государственных организациях"
//     organization: Optional[str] = Field(alias="name", default=None)
//     inn: Optional[str] = None

// class StateOrganizationsJson(BaseModel):
//     view: str = "Являлся государственным должностным лицом"
//     organization: Optional[str] = Field(alias="name", default=None)

// class PublicOfficeOrganizationsJson(BaseModel):
//     view: str = "Являлся государственным или муниципальным служащим"
//     organization: Optional[str] = Field(alias="name", default=None)
