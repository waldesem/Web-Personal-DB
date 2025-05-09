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

export interface User {
  id: string;
  fullname: string;
  username: string;
  email: string;
  pswd_create: string;
  change_pswd: boolean;
  blocked: boolean;
  deleted: boolean;
  created: string;
  attempt: string;
  region: string;
  role: string;
}

export interface Token {
  id: string;
  fullname: string;
  username: string;
  email: string;
  region: string;
  role: string;
  exp: number;
}

export interface Persons {
  id: string;
  surname: string;
  firstname: string;
  patronymic: string;
  birthday: string;
  birthplace: string;
  citizenship: string;
  dual: string;
  snils: string;
  inn: string;
  marital: string;
  addition: string;
  destination: string;
  editable: boolean;
  created: string;
  region: string;
  username: string;
  user_id: string;
}

export interface Relation {
  right_id: string;
  type: string;
}

export interface Relationship {
  left_id: string;
  type: string;
}

export interface Previous {
  id: string;
  surname: string;
  firstname: string;
  patronymic: string;
  changed: string;
  created: string;
  reason: string;
}

export interface Education {
  id: string;
  view: string;
  institution: string;
  finished: string;
  specialty: string;
  created: string;
}

export interface Staff {
  id: string;
  position: string;
  department: string;
  created: string;
}

export interface Passport {
  id: string;
  view: string;
  series: string;
  digits: string;
  agency: string;
  issue: string;
  created: string;
}

export interface Address {
  id: string;
  view: string;
  addresses: string;
  created: string;
}

export interface Contact {
  id: string;
  view: string;
  contact: string;
  created: string;
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
  created: string;
}

export interface Affilation {
  id: string;
  view: string;
  organization: string;
  inn: string;
  created: string;
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
  conclusion: string;
  comment: string;
  created: string;
}

export interface Pfo {
  id: string;
  theme: string;
  results: string;
  conclusion: string;
  user_id: string;
  created: string;
}

export interface Inquisition {
  id: string;
  theme: string;
  info: string;
  user_id: string;
  created: string;
}

export interface Needs {
  id: string;
  info: string;
  initiator: string;
  origins: string;
  user_id: string;
  created: string;
}

export interface Folders {
  name: string;
  path: string;
}

export interface Files {
  name: string;
  path: string;
}

export type DivsType =
  | Address
  | Affilation
  | Contact
  | Passport
  | Education
  | Previous
  | Staff
  | Work;

export type TabsType = Verification | Pfo | Inquisition | Needs;

export interface MappedCompType {
  [key: string]: [Component, Component]
};