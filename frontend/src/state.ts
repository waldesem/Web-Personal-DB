import { reactive } from "vue";
import { axiosAuth } from "@/auth";
import { router } from "@/router";
import { server } from "@/utilities";
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

export const stateToken = reactive({
  accessToken: "" as any,
  refreshToken: localStorage.getItem("refresh_token") as any,
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

export const stateAnketa = {
  anketa: reactive({
    resume: {} as Resume,
    previous: [] as Previous[],
    staff: [] as Staff[],
    document: [] as Document[],
    address: [] as Address[],
    contact: [] as Contact[],
    relation: [] as Relation[],
    workplace: [] as Work[],
    affilation: [] as Affilation[],
    check: [] as Verification[],
    robot: [] as Robot[],
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
      this.anketa.resume = response.data;

      if (["self", "send", "status"].includes(action)) {
        this.getResume("view");

        if (action === "status") {
          stateAlert.setAlert("alert-info", "Статус анкеты обновлен");
        }
        if (action === "self") {
          stateAlert.setAlert("alert-info", "Анкета назначена на себя");
        }
        if (action === "send") {
          stateAlert.setAlert("alert-success", "Анкета отправлена на проверку");
        }
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
        console.log(response.data);
        this.share.imageUrl = window.URL.createObjectURL(
          new Blob([response.data]
          )
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
      (this.anketa.resume.status_id === stateClassify.status["finish"] ||
        this.anketa.resume.status_id === stateClassify.status["robot"])
    ) {
      stateAlert.setAlert(
        "alert-warning",
        "Невозможно удалить проверку с текщим статусом"
      );
      return;
    }
    if (
      ["robot", "finish"].includes(
        stateClassify.status[this.anketa.resume["status_id"]]
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
    const inputElement = event.target as HTMLInputElement;
    if (inputElement && inputElement.files && inputElement.files.length > 0) {
      const maxSizeInBytes = 1024 * 1024; // 1MB
      for (let i = 0; i < inputElement.files.length; i++) {
        if (inputElement.files[i].size > maxSizeInBytes) {
          stateAlert.setAlert(
            "alert-warning",
            "File size exceeds the limit. Please select a smaller file."
          );
          inputElement.value = ""; // Reset the input field
          return;
        }
      }
      const formData = new FormData();
      formData.append("file", inputElement.files[0]);

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
