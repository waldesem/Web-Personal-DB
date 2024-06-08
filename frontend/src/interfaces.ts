export interface Resume {
  id: string;
  surname: string;
  firstname: string;
  patronymic: string;
  birthday: string;
  birthplace: string;
  country: string;
  ext_country: string;
  snils: string;
  inn: string;
  marital: string;
  addition: string;
  path: string;
  status: string;
  created: string;
  updated: string;
  region: string;
  user_id: string;
}

export interface Previous {
  id: string;
  surname: string;
  firstname: string;
  patronymic: string;
  date_change: string;
  reason: string;
}

export interface Education {
  id: string;
  view: string;
  name: string;
  finish: string;
  speciality: string;
}

export interface Staff {
  id: string;
  position: string;
  department: string;
}

export interface Document {
  id: string;
  view: string;
  series: string;
  number: string;
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

export interface Relation {
  id: string;
  relation: string;
  relation_id: string;
}

export interface Work {
  id: string;
  now_work: boolean;
  start_date: string;
  end_date: string;
  workplace: string;
  address: string;
  reason: string;
  position: string;
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
  comments: string;
  created: string;
  user_id: string;
}

export interface Pfo {
  id: string;
  theme: string;
  results: string;
  user_id: string;
  created: string;
  updated: string;
}

export interface Inquisition {
  id: string;
  theme: string;
  info: string;
  user_id: string;
  created: string;
  updated: string;
}

export interface Needs {
  id: string;
  info: string;
  initiator: string;
  source: string;
  user_id: string;
  created: string;
  updated: string;
}

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
  attempt: string;
  region: string;
  created: string;
  updated: string;
}

export interface Connection {
  id: string;
  name: string;
  company: string;
  city: string;
  fullname: string;
  phone: string;
  adding: string;
  mobile: string;
  mail: string;
  comment: string;
  data: string;
}
