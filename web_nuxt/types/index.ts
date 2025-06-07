export type Method =
  | "get"
  | "post"
  | "put"
  | "delete"
  | "patch"
  | "head"
  | "connect"
  | "options"
  | "trace";

export type DivItems =
  | "staffs"
  | "educations"
  | "workplaces"
  | "documents"
  | "addresses"
  | "contacts"
  | "previous"
  | "affilations";

export type TabItems = "checks" | "poligrafs" | "investigations" | "inquiries";

export type Regions =
  | "Главный офис"
  | "РЦ Юг"
  | "РЦ Запад"
  | "РЦ Урал"
  | "РЦ Восток";

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

export interface Token extends UserForm {
  id: string;
  region: Regions;
  role: "admin" | "api" | "user" | "guest";
  exp: number;
}

export interface User extends Omit<Token, "exp"> {
  pswd_create: string;
  change_pswd: boolean;
  blocked: boolean;
  deleted: boolean;
  created: string;
  attempt: string;
}

export interface Previous {
  id: string;
  surname: string;
  firstname: string;
  patronymic?: string;
  changed?: string;
  reason?: string;
}

export interface Persons extends Omit<Previous, "changed" | "reason"> {
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
  region: Regions;
  username: string;
  user_id: string;
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
  addresses: string;
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
  addresses: string;
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
  conclusion:
    | "СОГЛАСОВАНО"
    | "СОГЛАСОВАНО С КОММЕНТАРИЕМ"
    | "ОТКАЗАНО В СОГЛАСОВАНИИ"
    | "СНЯТ С ПРОВЕРКИ";
  comment: string;
  created: string;
}

export interface Pfo {
  id: string;
  theme: string;
  results: string;
  conclusion:
    | "БЕЗ ЗАМЕЧАНИЙ"
    | "С КОММЕНТАРИЯМИ"
    | "ОТКАЗ ОТ ПРОВЕРКИ"
    | "НЕГАТИВ";
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
