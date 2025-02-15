import { useStorage } from "@vueuse/core";
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
  Relation,
  Relationship,
  Staff,
  Verification,
  Work,
} from "@/types";


export const dataPerson = useStorage("dataPerson", {
  person: {} as Persons,
  relations: [] as Relation[],
  relationships: [] as Relationship[],
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
