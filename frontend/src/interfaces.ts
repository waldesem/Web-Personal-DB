export interface User {
  id: string;
  fullname: string;
  username: string;
  email: string;
  pswd_create: string;
  change_pswd: boolean;
  last_login: string;
  has_admin: boolean;
  blocked: boolean;
  deleted: boolean;
  created: string;
  attempt: string;
  region: string;
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
  path: string;
  status: string;
  created: string;
  region: string;
  user_id: string;
  username: User;
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
  name: string;
  finished: string;
  speciality: string;
  created: string;
}

export interface Staff {
  id: string;
  position: string;
  department: string;
  created: string;
}

export interface Document {
  id: string;
  view: string;
  series: string;
  number: string;
  agency: string;
  issue: string;
  created: string;
}

export interface Address {
  id: string;
  view: string;
  address: string;
  created: string;
}

export interface Contact {
  id: string;
  view: string;
  contact: string;
  created: string;
}

export interface Relation {
  id: string;
  relation: string;
  relation_id: string;
  created: string;
}

export interface Work {
  id: string;
  now_work: boolean;
  started: string;
  finished: string;
  workplace: string;
  address: string;
  reason: string;
  position: string;
  created: string;
}

export interface Affilation {
  id: string;
  view: string;
  name: string;
  inn: string;
  position: string;
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
  pfo: boolean;
  conclusion: string;
  comment: string;
  created: string;
  user_id: string;
  user: string;
}

export interface Pfo {
  id: string;
  theme: string;
  results: string;
  user_id: string;
  user: string;
  created: string;
}

export interface Inquisition {
  id: string;
  theme: string;
  info: string;
  user_id: string;
  user: string;
  created: string;
}

export interface Needs {
  id: string;
  info: string;
  initiator: string;
  user_id: string;
  user: string;
  created: string;
}

export interface Connection {
  id: string;
  view: string;
  company: string;
  city: string;
  fullname: string;
  phone: string;
  adding: string;
  mobile: string;
  email: string;
  comment: string;
  created: string;
}
