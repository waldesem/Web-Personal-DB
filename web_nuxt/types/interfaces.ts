export interface Login {
  username: string;
  password: string;
  new_pswd: string;
  conf_pswd: string;
}

export interface Token {
  id: number;
  fullname: string;
  username: string;
  role: string;
  region: string;
}

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
  user_id: string;
  username: string;
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

export interface Document {
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

export interface Relation {
  id: string;
  relation: string;
  relation_id: string;
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
  user_id: string;
  username: string;
}

export interface Pfo {
  id: string;
  theme: string;
  results: string;
  user_id: string;
  username: string;
  created: string;
}

export interface Inquisition {
  id: string;
  theme: string;
  info: string;
  user_id: string;
  username: string;
  created: string;
}

export interface Needs {
  id: string;
  info: string;
  initiator: string;
  origins: string;
  user_id: string;
  username: string;
  created: string;
}

export interface Profile {
  persons: Persons;
  previous: Previous[];
  educations: Education[];
  staffs: Staff[];
  documents: Document[];
  addresses: Address[];
  contacts: Contact[];
  relations: Relation[];
  workplaces: Work[];
  affilations: Affilation[];
  checks: Verification[];
  poligrafs: Pfo[];
  investigations: Inquisition[];
  inquiries: Needs[];
}

export interface Classes {
  regions: Record<string, unknown>;
  conclusions: Record<string, unknown>;
  relations: Record<string, unknown>;
  affiliates: Record<string, unknown>;
  educations: Record<string, unknown>;
  addresses: Record<string, unknown>;
  contacts: Record<string, unknown>;
  documents: Record<string, unknown>;
  poligrafs: Record<string, unknown>;
  roles: Record<string, unknown>;
}
