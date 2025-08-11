export type DivsItems =
  | "staffs"
  | "educations"
  | "workplaces"
  | "documents"
  | "addresses"
  | "contacts"
  | "previous"
  | "affilations";

export type PillsItems =
  | "checks"
  | "poligrafs"
  | "investigations"
  | "inquiries";

export interface Token {
  id: string;
  fullname: string;
  username: string;
  email: string;
  role: Roles;
  exp: number;
}

export interface User extends Token {
  pswd_create: string;
  change_pswd: boolean;
  blocked: boolean;
  deleted: boolean;
  created: string;
  attempt: string;
}

export interface Candidate {
  id: string;
  fullname: string;
  birthday: string;
  editable: boolean;
  created: string;
  username: string;
  total: number;
}

export interface Persons {
  id: string;
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
  destination?: string;
  editable: boolean;
  created: string;
  username: string;
  user_id: string;
}

export interface Previous {
  id: string;
  surname: string;
  firstname: string;
  patronymic?: string;
  changed?: string;
  reason?: string;
}
export interface Education {
  id: string;
  view: string;
  institution: string;
  finished: string;
  specialty: string;
}

export interface Staff {
  id: string;
  position: string;
  department: string;
}

export interface Passport {
  id: string;
  view: string;
  series: string;
  digits: string;
  agency: string;
  issue: string;
}

export interface Address {
  id: string;
  view: string;
  address: string;
}

export interface Contact {
  id: string;
  view: string;
  contact: string;
}

export interface Work {
  id: string;
  now_work: boolean;
  starts: string;
  finished: string;
  workplace: string;
  address: string;
  reason: string;
  position: string;
}

export interface Affilation {
  id: string;
  view: string;
  organization: string;
  inn: string;
}

export interface Verification {
  id: string;
  workplace: string;
  document: string;
  inn: string;
  debt: string;
  bankruptcy: string;
  bki: string;
  courts: string;
  affilation: string;
  terrorist: string;
  mvd: string;
  internet: string;
  cronos: string;
  cros: string;
  addition: string;
  conclusion: Conclusions;
  comment: string;
  created: string;
}

export interface Pfo {
  id: string;
  theme: string;
  results: string;
  conclusion: Decisions;
  created: string;
}

export interface Inquisition {
  id: string;
  theme: string;
  info: string;
  created: string;
}

export interface Needs {
  id: string;
  info: string;
  initiator: string;
  origins: string;
  created: string;
}

enum Roles {
  admin = "admin",
  api = "api",
  user = "user",
  guest = "guest",
}

export enum Conclusions {
  agreed = "СОГЛАСОВАНО",
  comments = "СОГЛАСОВАНО С КОММЕНТАРИЕМ",
  denied = "ОТКАЗАНО В СОГЛАСОВАНИИ",
  cancel = "СНЯТ С ПРОВЕРКИ",
}

export enum Decisions {
  agreed = "БЕЗ ЗАМЕЧАНИЙ",
  comments = "С КОММЕНТАРИЯМИ",
  cancel = "ОТКАЗ ОТ ПРОВЕРКИ",
  denied = "НЕГАТИВ",
}
