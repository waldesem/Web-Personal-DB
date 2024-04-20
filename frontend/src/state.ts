import { reactive } from 'vue'
import {
  Resume,
  Previous,
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
} from "@/interfaces";

export const stateAnketa = reactive({
  resume: <Resume>{},
  previous: [] as Array<Previous>,
  staff: [] as Array<Staff>,
  document: [] as Array<Document>,
  address: [] as Array<Address>,
  contact: [] as Array<Contact>,
  relation: [] as Array<Relation>,
  workplace: [] as Array<Work>,
  affilation: [] as Array<Affilation>,
  check: [] as Array<Verification>,
  robot: [] as Array<Robot>,
  poligraf: [] as Array<Pfo>,
  investigation: [] as Array<Inquisition>,
  inquiry: [] as Array<Needs>,
});

export const stateToken = reactive({
  accessToken: "" as string | null,
  refreshToken: "" as string | null,
});

export const stateUser = reactive({
  userId: "",
  fullName: "",
  userName: "",
  userRoles: [],
  hasAdmin: false,
});

export const stateClassify = reactive({
  status: <Record<string, any>>{},
  regions: <Record<string, any>>{},
  conclusions: <Record<string, any>>{},
  roles: <Record<string, any>>{},
  users: <Record<string, any>>{},
});
  
export const stateAlert = {
  alertMessage: reactive({
    attr: "",
    text: "",
  }),
  setAlert(attr: string = "", text: string = "") {
    this.alertMessage.attr = attr;
    this.alertMessage.text = text;
    setTimeout(() => {
      this.setAlert();
    }, 10000);
  },
};
  