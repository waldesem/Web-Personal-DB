import type {
  Address,
  Affilation,
  Contact,
  Education,
  Needs,
  Inquisition,
  Pfo,
  Passport,
  Persons,
  Previous,
  Staff,
  Token,
  Verification,
  Work,
} from "@/types";

export const stateUser = ref({} as Token);

export const statePerson = ref({
  person: {} as Persons,
  previous: [] as Previous[],
  educations: [] as Education[],
  staffs: [] as Staff[],
  documents: [] as Passport[],
  addresses: [] as Address[],
  contacts: [] as Contact[],
  workplaces: [] as Work[],
  affilations: [] as Affilation[],
  checks: [] as Verification[],
  poligrafs: [] as Pfo[],
  inquiries: [] as Needs[],
  investigations: [] as Inquisition[],
});
