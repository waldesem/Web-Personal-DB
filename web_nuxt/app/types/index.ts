// import type { AsyncDataRequestStatus } from "nuxt/app";

// export interface Status {
//   message: AsyncDataRequestStatus;
// }

export enum Actions {
  delete = "delete",
  block = "block",
  reset = "reset",
}

export enum Roles {
  admin = "admin",
  api = "api",
  user = "user",
  guest = "guest",
}

export enum Conclusions {
  agreed = "СОГЛАСОВАНО",
  comments = "СОГЛАСОВАНО С КОММЕНТАРИЕМ",
  cancel = "СНЯТ С ПРОВЕРКИ",
  denied = "ОТКАЗАНО В СОГЛАСОВАНИИ",
}

export enum Decisions {
  agreed = "БЕЗ ЗАМЕЧАНИЙ",
  comments = "С КОММЕНТАРИЯМИ",
  cancel = "ОТКАЗ ОТ ПРОВЕРКИ",
  denied = "НЕГАТИВ",
}

export interface Login {
  username: string;
  password: string;
  new_pswd: string;
  conf_pswd: string;
}

export interface UserForm {
  fullname: string;
  username: string;
  email: string;
}

export interface Session extends UserForm {
  id: string;
  role: Roles;
}

export interface User extends Session {
  pswd_create: string;
  change_pswd: boolean;
  blocked: boolean;
  deleted: boolean;
  created_at: string;
  updated_at: string;
  attempt: string;
}

export interface Person {
  surname: string;
  firstname: string;
  patronymic?: string;
  birthday: string;
  birthplace?: string;
  citizenship?: string;
  dual?: string;
  snils?: string;
  inn?: string;
  marital?: string;
  addition?: string;
}

export interface PersonExt extends Person {
  id: string;
  user_id: string;
  destination?: string;
  editable: boolean;
  locked: boolean;
  created_at: string;
  updated_at: string;
}

export interface PersonId {
  person_id: number | null;
}

export interface Candidate extends PersonExt {
  username: string;
  total: number;
}

export interface Previous {
  surname: string;
  firstname?: string;
  patronymic?: string;
  changed?: string;
  reason?: string;
}

export interface Id {
  id: string;
}

export interface PreviousExt extends Previous, Id {}

export interface Education {
  view?: string;
  institution: string;
  finished?: string;
  specialty: string;
}

export interface EducationExt extends Education, Id {}

export interface Staff {
  position: string;
  department?: string;
}

export interface StaffExt extends Staff, Id {}

export interface Passport {
  view: string;
  series?: string;
  digits: string;
  agency?: string;
  issue: string;
}

export interface PassportExt extends Passport, Id {}

export interface Address {
  view: string;
  address: string;
}

export interface AddressExt extends Address, Id {}

export interface Contact {
  view: string;
  contact: string;
}

export interface ContactExt extends Contact, Id {}

export interface Work {
  now_work: boolean;
  starts: string;
  finished: string;
  workplace: string;
  address?: string;
  reason?: string;
  position: string;
}

export interface WorkExt extends Work, Id {}

export interface Affilation {
  view: string;
  organization: string;
  inn?: string;
}

export interface AffilationExt extends Affilation, Id {}

export interface Verification {
  workplace?: string;
  document?: string;
  inn?: string;
  debt?: string;
  bankruptcy?: string;
  bki?: string;
  courts?: string;
  affilation?: string;
  terrorist?: string;
  mvd?: string;
  internet?: string;
  cronos?: string;
  addition?: string;
  conclusion: Conclusions;
  comment?: string;
}

export interface Extend extends Id {
  created_at: string;
  updated_at: string;
}

export interface VerificationExt extends Verification, Extend {}

export interface Pfo {
  theme: string;
  results: string;
  conclusion: Decisions;
}

export interface PfoExt extends Pfo, Extend {}

export interface Inquisition {
  theme: string;
  info: string;
}

export interface InquisitionExt extends Inquisition, Extend {}

export interface Needs {
  info: string;
  initiator: string;
}

export interface NeedsExt extends Needs, Extend {}

export interface Item {
  staffs: StaffExt;
  educations: EducationExt;
  workplaces: WorkExt;
  documents: PassportExt;
  addresses: AddressExt;
  contacts: ContactExt;
  affilations: AffilationExt;
  previous: PreviousExt;
  checks: VerificationExt;
  poligrafs: PfoExt;
  investigations: InquisitionExt;
  inquiries: NeedsExt;
}

export interface Items {
  staffs: StaffExt[];
  educations: EducationExt[];
  workplaces: WorkExt[];
  documents: PassportExt[];
  addresses: AddressExt[];
  contacts: ContactExt[];
  affilations: AffilationExt[];
  previous: PreviousExt[];
  checks: VerificationExt[];
  poligrafs: PfoExt[];
  investigations: InquisitionExt[];
  inquiries: NeedsExt[];
}
