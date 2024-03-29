export interface Anketa {
  resume: Resume,
  staffs: Staff[],
  documents: Document[],
  addresses: Address[],
  contacts: Contact[],
  relations: Relation[],
  affilations: Affilation[],
  workplaces: Work[],
  checks: Verification[],
  robots: Robot[],
  poligraf: Pfo[],
  investigations: Inquisition[],
  inquiries: Needs[],
}

export interface Resume {
  id: string;
  region_id: string;
  user_id: string;
  surname: string;
  firstname: string;
  patronymic: string;
  previous: string;
  birthday: string;
  birthplace: string;
  country: string;
  ext_country: string;
  snils: string;
  inn: string;
  education: string;
  marital: string;
  addition: string;
  path: string;
  status_id: string;
  created: string;
  updated: string;
  request_id: string;
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
  region: string;
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
  deadline: string;
}

export interface Verification {
  id: string;
  workplace: string;
  employee: string;
  document: string;
  inn: string;
  debt: string;
  bankruptcy: string;
  bki: string;
  courts: string;
  affiliation: string;
  terrorist: string;
  mvd: string;
  internet: string;
  cronos: string;
  cros: string;
  addition: string;
  pfo: string;
  conclusion: string;
  comments: string;
  deadline: string;
  officer: string;
}

export interface Robot {
  id: string;
  employee: string;
  document: string;
  inn: string;
  debt: string;
  bankruptcy: string;
  bki: string;
  courts: string;
  affiliation: string;
  terrorist: string;
  mvd: string;
  deadline: string;
}

export interface Pfo {
  id: string;
  theme: string;
  results: string;
  officer: string;
  deadline: string;
}

export interface Inquisition {
  id: string;
  theme: string;
  info: string;
  officer: string;
  deadline: string;
}

export interface Needs {
  id: string;
  info: string;
  initiator: string;
  source: string;
  officer: string;
  deadline: string;
}

export interface Message {
  message: string;
  created: string;
}

export interface Role {
  id: string;
  role: string;
}

export interface User {
  id: string;
  fullname: string;
  username: string;
  email: string;
  pswd_create: string;
  pswd_change: string;
  last_login: string;
  roles: Role[];
  blocked: boolean;
  deleted: boolean;
  attempt: string;
}

export interface Message {
  message: string;
  created: string;
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

export interface ConnectionForm {
  name: string;
  company: string;
  city: string;
  fullname: string;
  phone: string;
  adding: string;
  mobile: string;
  mail: string;
  comment: string;
}
