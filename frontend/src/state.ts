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
  status: <Record<string, any>>{},
  regions: <Record<string, any>>{},
  conclusions: <Record<string, any>>{},
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
    education: [] as Education[],
    staff: [] as Staff[],
    document: [] as Document[],
    address: [] as Address[],
    contact: [] as Contact[],
    relation: [] as Relation[],
    workplace: [] as Work[],
    affilation: [] as Affilation[],
    check: [] as Verification[],
    poligraf: [] as Pfo[],
    investigation: [] as Inquisition[],
    inquiry: [] as Needs[],
  }),
  share: reactive({
    candId: "" as string,
    imageUrl: "" as string,
    printPage: false,
  }),

  async getResume(action = "view"): Promise<void> {
    if (action === "status") {
      if (
        !confirm(
          "Вы действительно хотите изменить статус? USER_ID анкеты будет сброшен"
        )
      ) {
        return;
      }
    }
    if (action === "send") {
      if (!confirm("Вы действительно хотите отправить анкету на проверку?")) {
        return;
      }
    }
    if (action === "self") {
      if (!confirm("Вы действительно назначить проверку кандидата на себя?")) {
        return;
      }
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
      const { message } = response.data;

      switch (message) {
        case "status":
          stateAlert.setAlert("alert-info", "Статус анкеты обновлен");
          this.getResume();
          break;
        case "self":
          stateAlert.setAlert("alert-info", "Анкета назначена на себя");
          this.getResume();
          break;
        case "send":
          stateAlert.setAlert("alert-success", "Анкета отправлена на проверку");
          this.getResume();
          break;
        case "error":
          stateAlert.setAlert("alert-danger", "Ошибка обработки");
          this.getResume();
          break;
        default:
          this.anketa.resume = message;
          break;
      }
    } catch (error) {
      console.error(error);
      stateAlert.setAlert("alert-danger", `Ошибка обработки ${error}`);
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
      stateAlert.setAlert("alert-danger", `Возникла ошибка ${error}`);
    }
  },

  async deleteItem(id: string, param: string): Promise<void> {
    if (!confirm(`Вы действительно хотите удалить запись?`)) return;
    if (
      param === "check" &&
      (this.anketa.resume.status === stateClassify.status["finish"] ||
        this.anketa.resume.status === stateClassify.status["robot"])
    ) {
      stateAlert.setAlert(
        "alert-warning",
        "Невозможно удалить проверку с текщим статусом"
      );
      return;
    }
    if (
      ["robot", "finish"].includes(
        stateClassify.status[this.anketa.resume["status"]]
      )
    ) {
      stateAlert.setAlert(
        "alert-warning",
        "Нельзя удалить запись с текущим статусом"
      );
      return;
    }
    try {
      const response = await axiosAuth.delete(`${server}/${param}/${id}`);
      console.log(response.status);

      param === "resume"
        ? router.push({ name: "persons" })
        : this.getItem(param);

      stateAlert.setAlert("alert-info", `Запись с ID ${id} удалена`);
    } catch (error) {
      console.error(error);
    }
  },

  async submitFile(event: Event, param: string): Promise<void> {
    const formData = new FormData();
    const inputElement = event.target as HTMLInputElement;
    if (inputElement && inputElement.files && inputElement.files.length > 0) {
      const maxSizeInBytes = 2 * 1024 * 1024; // 1MB
      for (let i = 0; i < inputElement.files.length; i++) {
        if (inputElement.files[i].size > maxSizeInBytes) {
          stateAlert.setAlert(
            "alert-warning",
            "File size exceeds the limit. Please select a smaller file."
          );
          inputElement.value = ""; // Reset the input field
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
        console.error(error);
      }
    } else {
      stateAlert.setAlert("alert-warning", "Ошибка при загрузке файла");
    }
  },
};
