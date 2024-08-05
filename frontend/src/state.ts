import { reactive } from "vue";
import { axiosAuth } from "@/auth";
import { router } from "@/router";
import * as interfaces from "@/interfaces";

// export const server = "http://localhost:5000";
export const server = "";

export const stateUser = {
  user: reactive({
    userId: "",
    username: "",
    role: "",
    region: "",
  }),
  async getCurrentUser(): Promise<void> {
    try {
      const auth = await axiosAuth.get(`${server}/auth`);
      const user = auth.data;
      Object.assign(this.user, {
        userId: user["id"],
        username: user["username"],
        role: user["role"],
        region: user["region"],
      })
      await stateClassify.getClassify();
      router.push({ name: "persons" });
    } catch (error: any) {
      router.push({ name: "login" });
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
    roles: <Record<string, any>>{},
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
      console.log(this.classes);
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

export const statePersons = {
  persons: reactive({
    candidates: <interfaces.Persons[]>[],
    page: 1,
    prev: false,
    next: true,
    search: "",
    updated: `${new Date().toLocaleDateString(
      "ru-RU"
    )} в ${new Date().toLocaleTimeString("ru-RU")}`,
  }),

  async getCandidates(page = 1): Promise<void> {
    if (this.persons.page < 1) {
      this.persons.page = 1;
      return;
    } else {
      this.persons.page = page;
    }
    try {
      const response = await axiosAuth.get(
        `${server}/index/${this.persons.page}`,
        {
          params: {
            search: this.persons.search,
          },
        }
      );
      [this.persons.candidates, this.persons.next, this.persons.prev] =
        response.data;

      this.persons.updated = `${new Date().toLocaleDateString(
        "ru-RU"
      )} в ${new Date().toLocaleTimeString("ru-RU")}`;
    } catch (error: any) {
      console.error(error);
    }
  },
};

export const stateAnketa = {
  anketa: reactive({
    persons: {} as interfaces.Persons,
    previous: [] as interfaces.Previous[],
    educations: [] as interfaces.Education[],
    staffs: [] as interfaces.Staff[],
    documents: [] as interfaces.Document[],
    addresses: [] as interfaces.Address[],
    contacts: [] as interfaces.Contact[],
    relations: [] as interfaces.Relation[],
    workplaces: [] as interfaces.Work[],
    affilations: [] as interfaces.Affilation[],
    checks: [] as interfaces.Verification[],
    poligrafs: [] as interfaces.Pfo[],
    investigations: [] as interfaces.Inquisition[],
    inquiries: [] as interfaces.Needs[],
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
    const image = await axiosAuth.get(`${server}/image`, {
      params: {
        image: this.anketa.persons.destination,
      },
      responseType: "blob",
    });
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
      for (let file of inputElement.files) {
        if (file.size < (1024 * 1024) * 2) {
          formData.append("file", file);
        }
      }
      try {
        const response = await axiosAuth.post(
          `${server}/file/${param}/${itemId}`,
          formData
        );
        console.log(response.status);
        if (param === "persons") {
          statePersons.getCandidates(1);
        } else if (param === "image") {
          this.getImage();
        } else if (param === "anketa") {
          this.getItem("persons");
        } else this.getItem(param);

        stateAlert.setAlert(
          "alert-success",
          "Файл или файлы успешно загружены"
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
