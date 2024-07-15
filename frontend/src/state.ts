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

export const stateUser = reactive({
  userId: "",
  username: "",
  hasAdmin: false,
  region: ""
});

export const stateClassify = reactive({
  regions: <Record<string, any>>{},
  conclusions: <Record<string, any>>{},
  relations: <Record<string, any>>{},
  affilations: <Record<string, any>>{},
  educations: <Record<string, any>>{},
  addresses: <Record<string, any>>{},
  contacts: <Record<string, any>>{},
  documents: <Record<string, any>>{},
  poligrafs: <Record<string, any>>{},
});

export const stateAlert = {
  alertMessage: reactive({
    attr: "",
    text: "",
    show: false,
  }),
  setAlert(attr: string, text: string) {
    this.alertMessage.show = true;
    this.alertMessage.attr = attr;
    this.alertMessage.text = text;
    setTimeout(() => {
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

  async getItem(param: string, action = "view"): Promise<void> {
    if (
      action === "self" &&
      !confirm(
        "Вы действительно хотите включить/выключить режим правки"
      )
    ) {
      return;
    }
    try {
      const response =
        param === "image"
          ? await axiosAuth.get(`${server}/image/${this.share.candId}`, {
              responseType: "blob",
            })
          : await axiosAuth.get(`${server}/${param}/${this.share.candId}`, {
              params: {
                action: action,
              },
            });
      if (param === "image") {
        this.share.imageUrl = window.URL.createObjectURL(
          new Blob([response.data])
        );
      } else {
        this.anketa[param as keyof typeof this.anketa] = response.data;
      }
      if (action === "self") {
        stateAlert.setAlert("alert-info", "Режим проверки включен/отключен");
      }
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

  async submitFile(
    event: Event,
    param: string,
    itemId: string
  ): Promise<void> {
    const formData = new FormData();
    const inputElement = event.target as HTMLInputElement;
    if (inputElement && inputElement.files) {
      for (let i = 0; i < inputElement.files.length; i++) {
        if (inputElement.files[i].size > 10 * 1024 * 1024) {
          stateAlert.setAlert(
            "alert-warning",
            "Превышен максимальный размер файла"
          );
          inputElement.value = "";
          return;
        } else {
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
          this.getItem(param);
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
  }
}
