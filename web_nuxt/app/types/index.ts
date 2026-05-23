import type { InputProps, SelectProps, TextareaProps } from "@nuxt/ui";

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

export type TableColumns<T> = {
  name: keyof T;
  header: string;
  cell?: (row: T) => string;
};

export type ItemFields<T> = {
  key: keyof T;
  label: string;
  slot?: boolean;
  div?: (row: T) => string;
  component?: (row: T) => Component;
};

export type FormElementAttrs = {
  input: InputProps;
  select: SelectProps;
  textarea: TextareaProps;
};

export type FormFields<T> = {
  [K in keyof FormElementAttrs]: {
    element?: K;
    key: keyof T;
    label: string;
    props: Omit<FormElementAttrs[K], "modelValue" | "defaultValue">;
  };
}[keyof FormElementAttrs];

export interface Auth {
  message: string;
  access_token: string;
  refresh_token: string;
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
  id: number;
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
  user_id: string;
  destination?: string;
  created_at: string;
  updated_at: string;
}

export interface Candidate extends Person {
  username: string;
  total: number;
}

export interface Previous {
  id: string;
  surname: string;
  firstname?: string;
  patronymic?: string;
  changed?: string;
  reason?: string;
}

export interface Education {
  id: string;
  view?: string;
  institution: string;
  finished?: string;
  specialty: string;
}

export interface Staff {
  id: string;
  position: string;
  department?: string;
}

export interface Passport {
  id: string;
  view: string;
  series?: string;
  digits: string;
  agency?: string;
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
  address?: string;
  reason?: string;
  position: string;
}

export interface Affilation {
  id: string;
  view: string;
  organization: string;
  inn?: string;
  activity?: string;
}

export interface Verification {
  id: string;
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
  created_at: string;
  updated_at: string;
}

export interface Pfo {
  id: string;
  theme: string;
  results: string;
  conclusion: Decisions;
  created_at: string;
  updated_at: string;
}

export interface Inquisition {
  id: string;
  theme: string;
  info: string;
  created_at: string;
  updated_at: string;
}

export interface Needs {
  id: string;
  info: string;
  initiator: string;
  created_at: string;
  updated_at: string;
}

export type Items = {
  addresses: Address;
  affilations: Affilation;
  checks: Verification;
  contacts: Contact;
  documents: Passport;
  educations: Education;
  inquiries: Needs;
  investigations: Inquisition;
  person: Person;
  poligrafs: Pfo;
  previous: Previous;
  staffs: Staff;
  workplaces: Work;
};
