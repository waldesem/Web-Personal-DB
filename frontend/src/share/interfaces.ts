interface Candidate {
  id: number;
  fullname: string;
  region_id: number;
  birthday: string;
  status: string;
  create: string;
};

interface Resume {
  id: string;
  category: string;
  region_id: string;
  fullname: string;
  previous: string;
  birthday: string;
  birthplace: string;
  country: string;
  snils: string;
  inn: string;
  education: string;
  addition: string;
  path: string;
  status: string;
  create: string;
  update: string;
  request_id: string;
};

interface Document {
  id: string;
  view: string;
  series: string;
  number: string;
  agency: string;
  issue: string;
};

interface Address {
  id: string;
  view: string;
  region: string;
  address: string;
};

interface Contact {
  id: string;
  view: string;
  contact: string;
};

interface Work {
  id: string;
  start_date: string;
  end_date: string;
  now_work: boolean;
  workplace: string;
  address: string;
  position: string;
};

interface Staff {
  id: string;
  position: string;
  department: string;
};

interface Relation {
  id: string;
  relation: string;
  relation_id: string;
};

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
  pfo: boolean;
  conclusion: string;
  comments: string;
  deadline: string;
  officer: string;
};

interface Register {
  id: string;
  comments: string;
  decision: string;
  supervisor: string;
  deadline: string;
};

interface Pfo {
  id: string;
  theme: string;
  results: string;
  officer: string;
  deadline: string;
};

interface Inquisition {
  id: string;
  theme: string;
  info: string;
  officer: string;
  deadline: string;
};

interface Needs {
  id: string;
  info: string;
  initiator: string;
  source: string;
  officer: string;
  deadline: string;
};

interface Group {
  id: string,
  group: string
};

interface Role {
  id: string,
  role: string
};

interface User {
  id: string,
  fullname: string,
  username: string,
  email: string,
  region_id: string,
  pswd_create: string,
  pswd_change: string,
  last_login: string,
  roles: Role[],
  groups: Group[],
  blocked: string,
  attempt: string
};

interface Message {
  attrAlert: string,
  textAlert: string
};

interface Chart {
  labels: string[];
  datasets: {
    label: string;
    backgroundColor: string[];
    data: number[];
  }[];
};

export type {
  Candidate,
  Resume, 
  Document, 
  Address, 
  Contact, 
  Work, 
  Staff, 
  Relation, 
  Verification, 
  Register, 
  Pfo, 
  Inquisition, 
  Needs,
  User,
  Message,
  Chart
};