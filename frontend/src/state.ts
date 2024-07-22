import { reactive } from "vue";
import { axiosAuth } from "@/auth";
import { router } from "@/router";
import {
  Persons,
  Previous,
  Education,
  Staff,
  Document,
  Address,
  Contact,
  Relation,
  Work,
  Affilation,
  Verification,
  Pfo,
  Inquisition,
  Needs,
} from "@/interfaces";

// export const server = "http://localhost:5000";
export const server = "";

export const stateUser = {
  user: reactive({
    userId: "",
    username: "",
    hasAdmin: false,
    region: "",
  }),
  async getCurrentUser(): Promise<void> {
    try {
      const auth = await axiosAuth.get(`${server}/auth`);
      const user = auth.data;
      this.user.userId = user["id"];
      this.user.username = user["username"];
      this.user.hasAdmin = user["has_admin"];
      this.user.region = user["region"];
      await stateClassify.getClassify();
      router.push({ name: "persons" });
    } catch (error: any) {
      console.error(error);
    }
  },
};

export const stateClassify = {
  classes: reactive({
    regions: <Record<string, any>>{},
    conclusions: <Record<string, any>>{},
    relations: <Record<string, any>>{},
    affilations: <Record<string, any>>{},
    educations: <Record<string, any>>{},
    addresses: <Record<string, any>>{},
    contacts: <Record<string, any>>{},
    documents: <Record<string, any>>{},
    poligrafs: <Record<string, any>>{},
  }),
  async getClassify(): Promise<void> {
    try {
      const classes = await axiosAuth.get(`${server}/classes`);
      const resp = classes.data;
      const classifyKeys = Object.keys(this.classes);
      for (let i = 0; i < classifyKeys.length; i++) {
        this.classes[classifyKeys[i] as keyof typeof stateClassify.classes] =
          resp[i];
      }
    } catch (error: any) {
      console.error(error);
    }
  },
};

export const stateAlert = {
  alertMessage: reactive({
    attr: "",
    text: "",
    show: false,
    timeOut: 0,
  }),
  setAlert(attr: string, text: string) {
    window.clearTimeout(this.alertMessage.timeOut);
    this.alertMessage.show = true;
    this.alertMessage.attr = attr;
    this.alertMessage.text = text;
    this.alertMessage.timeOut = window.setTimeout(() => {
      this.alertMessage.show = false;
    }, 10000);
  },
};

export const stateAnketa = {
  anketa: reactive({
    persons: {} as Persons,
    previous: [] as Previous[],
    educations: [] as Education[],
    staffs: [] as Staff[],
    documents: [] as Document[],
    addresses: [] as Address[],
    contacts: [] as Contact[],
    relations: [] as Relation[],
    workplaces: [] as Work[],
    affilations: [] as Affilation[],
    checks: [] as Verification[],
    poligrafs: [] as Pfo[],
    investigations: [] as Inquisition[],
    inquiries: [] as Needs[],
  }),
  share: reactive({
    candId: "" as string,
    imageUrl: "" as string,
  }),

  async getItem(item: string, action = "view"): Promise<void> {
    if (
      action === "self" &&
      !confirm("Вы действительно хотите включить/выключить режим правки")
    ) {
      return;
    }
    try {
      const response = await axiosAuth.get(
        `${server}/${item}/${this.share.candId}`,
        {
          params: {
            action: action,
          },
        }
      );
      this.anketa[item as keyof typeof this.anketa] = response.data;
      if (action === "self") {
        stateAlert.setAlert("alert-info", "Режим проверки включен/отключен");
      }
    } catch (error: any) {
      console.error(error);
    }
  },

  async getImage() {
    const image = await axiosAuth.get(
      `${server}/image/${this.anketa.persons.destination}`,
      {
        responseType: "blob",
      }
    );
    this.share.imageUrl = window.URL.createObjectURL(new Blob([image.data]));
  },

  async changeRegion(): Promise<void> {
    if (!confirm("Вы действительно хотите изменить регион?")) return;
    try {
      const response = await axiosAuth.get(
        `${server}/region/${this.share.candId}`,
        {
          params: {
            region: this.anketa.persons["region"],
          },
        }
      );
      console.log(response.status);
      this.getItem("persons");
    } catch (error: any) {
      console.error(error);
    }
  },

  async updateItem(param: string, form: Object): Promise<void> {
    try {
      const response = await axiosAuth.post(
        `${server}/${param}/${this.share.candId}`,
        form
      );
      console.log(response.status);
      this.getItem(param);
      stateAlert.setAlert("alert-success", "Запись успешно добавлена");
    } catch (error: any) {
      console.error(error);
    }
  },

  async deleteItem(id: string, param: string): Promise<void> {
    if (!confirm(`Вы действительно хотите удалить запись?`)) return;
    try {
      const response = await axiosAuth.delete(`${server}/${param}/${id}`);
      console.log(response.status);
      param === "persons"
        ? router.push({ name: "persons" })
        : this.getItem(param);
      stateAlert.setAlert("alert-info", `Запись с ID ${id} удалена`);
    } catch (error: any) {
      console.error(error);
    }
  },

  async submitFile(event: Event, param: string, itemId: string): Promise<void> {
    const formData = new FormData();
    const inputElement = event.target as HTMLInputElement;
    if (inputElement && inputElement.files) {
      for (let i = 0; i < inputElement.files.length; i++) {
        if (inputElement.files[i].size > 1024 * 1024) {
          stateAlert.setAlert(
            "alert-warning",
            "Превышен максимальный размер файла"
          );
          formData.append("file", inputElement.files[i]);
        }
      }
      try {
        const response = await axiosAuth.post(
          `${server}/file/${param}/${itemId}`,
          formData
        );
        console.log(response.status);
        if (param === "image") {
          this.getImage();
        }
        if (param === "persons") {
          const { person_id } = response.data;
          router.push({ name: "profile", params: { id: person_id } });
        }
        stateAlert.setAlert(
          "alert-success",
          "Файл или файлы успешно загружен/добавлены"
        );
      } catch (error: any) {
        console.error(error);
      }
    } else {
      stateAlert.setAlert("alert-warning", "Ошибка при загрузке файла");
    }
  },

  async submitResume(action: string, form: Object): Promise<void> {
    if (action == "create") {
      try {
        const response = await axiosAuth.post(`${server}/resume`, form);
        const { person_id } = response.data;
        router.push({ name: "profile", params: { id: person_id } });
        stateAlert.setAlert("alert-success", "Данные успешно добавлены");
      } catch (error) {
        stateAlert.setAlert("alert-danger", `Возникла ошибка ${error}`);
      }
    } else {
      this.updateItem("persons", form);
    }
  },
};
