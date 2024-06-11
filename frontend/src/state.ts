import { reactive, ref } from "vue";
import { axiosAuth } from "@/auth";
import { router } from "@/router";
import { server } from "@/utilities";
import {
  Resume,
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

export const stateUser = reactive({
  userId: "",
  fullname: "",
  username: "",
  region: "",
  hasAdmin: false,
});

export const userToken = ref(localStorage.getItem("user_token") as any) || "";

export const stateClassify = reactive({
  regions: <Record<string, any>>{},
  status: <Record<string, any>>{},
  conclusions: <Record<string, any>>{},
  relations: <Record<string, any>>{},
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

export const stateAnketa = {
  anketa: reactive({
    resume: {} as Resume,
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
    printPage: false,
  }),

  async getResume(action = "view"): Promise<void> {
    if (
      action === "self" &&
      !confirm("Вы действительно назначить проверку кандидата на себя?")
    ) {
      return;
    }
    try {
      const response = await axiosAuth.get(
        `${server}/resume/${this.share.candId}`,
        {
          params: {
            action: action,
          },
        }
      );
      this.anketa.resume = response.data;
      if (action === "self") {
        stateAlert.setAlert("alert-info", "Анкета назначена на себя");
      }
    } catch (error) {
      console.error(error);
      stateAlert.setAlert("alert-danger", `Ошибка: ${error}`);
    }
  },

  async getItem(param: string): Promise<void> {
    try {
      const response =
        param === "image"
          ? await axiosAuth.get(`${server}/image/${this.share.candId}`, {
              responseType: "blob",
            })
          : await axiosAuth.get(`${server}/${param}/${this.share.candId}`);

      if (param === "image") {
        this.share.imageUrl = window.URL.createObjectURL(
          new Blob([response.data])
        );
      } else {
        this.anketa[param as keyof typeof this.anketa] = response.data;
      }
    } catch (error) {
      console.error(error);
      stateAlert.setAlert("alert-danger", `Ошибка: ${error}`);
    }
  },

  async updateItem(
    action: string,
    param: string,
    itemId: string,
    form: Object
  ): Promise<void> {
    try {
      const response =
        action === "create"
          ? await axiosAuth.post(
              `${server}/${param}/${this.share.candId}`,
              form
            )
          : await axiosAuth.patch(`${server}/${param}/${itemId}`, form);

      console.log(response.status);
      stateAlert.setAlert("alert-success", "Данные успешно обновлены");
      this.getItem(param);
    } catch (error) {
      stateAlert.setAlert("alert-danger", `Ошибка: ${error}`);
    }
  },

  async deleteItem(id: string, param: string): Promise<void> {
    if (!confirm(`Вы действительно хотите удалить запись?`)) return;
    try {
      const response = await axiosAuth.delete(`${server}/${param}/${id}`);
      console.log(response.status);
      param === "resume"
        ? router.push({ name: "persons" })
        : this.getItem(param);
      stateAlert.setAlert("alert-info", `Запись с ID ${id} удалена`);
    } catch (error) {
      stateAlert.setAlert("alert-danger", `Ошибка: ${error}`);
    }
  },

  async submitFile(event: Event, param: string): Promise<void> {
    const formData = new FormData();
    const inputElement = event.target as HTMLInputElement;
    if (inputElement && inputElement.files) {
      for (let i = 0; i < inputElement.files.length; i++) {
        if (inputElement.files[i].size > 10 * 1024 * 1024) {
          stateAlert.setAlert("alert-warning","Превышен максимальный размер файла");
          inputElement.value = "";
          return;
        } else {
          formData.append("file", inputElement.files[i]);
        }
      }
      try {
        const response = await axiosAuth.post(
          `${server}/file/${param}/${this.share.candId}`,
          formData
        );
        console.log(response.status);
        if (param === "image") {
          this.getItem(param);
        }
        stateAlert.setAlert(
          "alert-success",
          "Файл или файлы успешно загружен/добавлены"
        );
      } catch (error) {
        stateAlert.setAlert("alert-danger", `Ошибка: ${error}`);
      }
    } else {
      stateAlert.setAlert("alert-warning", "Ошибка при загрузке файла");
    }
  },
};
