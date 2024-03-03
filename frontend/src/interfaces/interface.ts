interface Candidate {
  id: number;
  fullname: string;
  region_id: number;
  birthday: string;
  status_id: string;
  created: string;
}

interface Resume {
  id: string;
  category_id: string;
  region_id: string;
  user_id: string;
  fullname: string;
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

interface Staff {
  id: string;
  position: string;
  department: string;
}

interface Document {
  id: string;
  view: string;
  series: string;
  number: string;
  agency: string;
  issue: string;
}

interface Address {
  id: string;
  view: string;
  region: string;
  address: string;
}

interface Contact {
  id: string;
  view: string;
  contact: string;
}

interface Relation {
  id: string;
  relation: string;
  relation_id: string;
}

interface Work {
  id: string;
  start_date: string;
  end_date: string;
  workplace: string;
  address: string;
  reason: string;
  position: string;
}

interface Affilation {
  id: string;
  view: string;
  name: string;
  inn: string;
  position: string;
  deadline: string;
}

interface Verification {
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

interface Robot {
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

interface Pfo {
  id: string;
  theme: string;
  results: string;
  officer: string;
  deadline: string;
}

interface Inquisition {
  id: string;
  theme: string;
  info: string;
  officer: string;
  deadline: string;
}

interface Needs {
  id: string;
  info: string;
  initiator: string;
  source: string;
  officer: string;
  deadline: string;
}

interface Message {
  message: string;
  created: string;
}

interface Role {
  id: string;
  role: string;
}

interface User {
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

interface Message {
  message: string;
  created: string;
}

interface Connection {
  id: string;
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

export type {
  Candidate,
  Resume,
  Staff,
  Document,
  Address,
  Contact,
  Relation,
  Work,
  Affilation,
  Verification,
  Robot,
  Pfo,
  Inquisition,
  Needs,
  Message,
  Role,
  User,
  Connection,
};
