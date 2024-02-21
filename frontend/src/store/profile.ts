import { ref } from "vue";
import { defineStore } from "pinia";
import { classifyStore } from "@store/classify";
import { authStore } from "@/store/token";
import { alertStore } from "@store/alert";
import { server, clearForm } from "@utilities/utils";
import router from "@/router/router";

export const profileStore = defineStore("profileStore", () => {
  const storeAuth = authStore();
  const storeAlert = alertStore();
  const classifyApp = classifyStore();

  interface Resume {
    id: string;
    category_id: string;
    region_id: string;
    fullname: string;
    previous: string;
    birthday: string;
    birthplace: string;
    country: string;
    ext_country: string;
    snils: string;
    inn: string;
    education: string;
    marital: string;
    addition: string;
    path: string;
    status_id: string;
    created: string;
    updated: string;
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
    workplace: string;
    address: string;
    reason: string;
    position: string;
  };
  
  interface Relation {
    id: string;
    relation: string;
    relation_id: string;
  };
  
  interface Affilation {
    id: string;
    view: string;
    name: string;
    inn: string;
    position: string;
    deadline: string;
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
    pfo: string;
    conclusion: string;
    comments: string;
    deadline: string;
    officer: string;
  };
  
  interface Robot {
    id: string;
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
  
  const dataProfile = ref({
    candId: "",
    itemId: "",
    item: "",
    action: "",
    url: "",
    spinner: false,
    form: <Record<string, any>>{},

    getImage: async function (): Promise<void> {
      try {
        const response = await storeAuth.axiosInstance.get(
          `${server}/file/get/${this.candId}`,
          { responseType: "blob" }
        );
        this.url = window.URL.createObjectURL(new Blob([response.data]));
      } catch (error) {
        console.error(error);
      }
    },

    submitFile: async function (
      event: Event,
      flag: string,
      idItem: string = "0"
    ): Promise<void> {
      const inputElement = event.target as HTMLInputElement;
      if (inputElement && inputElement.files && inputElement.files.length > 0) {
        const maxSizeInBytes = 1024 * 1024; // 1MB
        for (let i = 0; i < inputElement.files.length; i++) {
          if (inputElement.files[i].size > maxSizeInBytes) {
            storeAlert.alertMessage.setAlert(
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
          const response = await storeAuth.axiosInstance.post(
            `${server}/file/${flag}/${idItem}`,
            formData
          );
          console.log(response.status);

          if (flag === "image") {
            this.getImage();
          } else {
            storeAlert.alertMessage.setAlert(
              "alert-success",
              "Файл или файлы успешно загружен/добавлены"
            );
          }
        } catch (error) {
          console.error(error);
        }
      } else {
        storeAlert.alertMessage.setAlert(
          "alert-warning",
          "Ошибка при загрузке файла"
        );
      }
    },

    openForm: function (item: string, action: string, idItem = "", form = {}) {
      this.item = item;
      this.action = action;
      if (action == "create") {
        this.form = {};
      } else {
        this.itemId = idItem;
        this.form = form;
      }
    },

    cancelEdit: function (): void {
      clearForm(this.form);
      this.action = "";
    },
  });

  const dataResume = ref({
    resume: <Resume>{},
    getResume: async function (action = "view"): Promise<void> {
      if (action === "status") {
        if (!confirm("Вы действительно хотите изменить статус резюме?")) {
          return;
        }
      };
      if (action === "send") {
        if (!confirm("Вы действительно хотите отправить анкету на проверку?")) {
          return;
        }
      };
      try {
        const response = await storeAuth.axiosInstance.get(
          `${server}/resume/${dataProfile.value.candId}`,
          {
            params: {
              action: action,
            },
          }
        );
        this.resume = response.data;

        if (action === "status") {
          storeAlert.alertMessage.setAlert(
            "alert-info",
            "Статус анкеты обновлен"
          );
        }
        if (action === "send") {
          storeAlert.alertMessage.setAlert(
            "alert-success",
            "Анкета отправлена на проверку"
          );
          dataProfile.value.spinner = false;
          window.scrollTo(0, 0);
        }
      } catch (error) {
        console.error(error);
        storeAlert.alertMessage.setAlert(
          "alert-danger",
          `Ошибка обработки ${error}`
        );
      }
    },

    submitResume: async function (): Promise<void> {
      try {
        const response =
          dataProfile.value.action === "create"
            ? await storeAuth.axiosInstance.post(
                `${server}/resume`,
                dataProfile.value.form
              )
            : await storeAuth.axiosInstance.patch(
                `${server}/resume`,
                dataProfile.value.form
              );
        const { message } = response.data;
        storeAlert.alertMessage.setAlert(
          dataProfile.value.action === "create"
            ? "alert-success"
            : "alert-info",
          dataProfile.value.action === "create"
            ? "Анкета успешно добавлена"
            : "Анкета успешно обновлена"
        );
        if (dataProfile.value.action === "create") {
          dataProfile.value.candId = message;
          router.push({ name: "profile", params: { id: message } });
        } else {
          this.getResume();
        }
      } catch (error) {
        console.error(error);
      }
    },

    uploadResume: async function (event: Event): Promise<void> {
      const inputElement = event.target as HTMLInputElement;
      if (inputElement && inputElement.files && inputElement.files.length > 0) {
        const formData = new FormData();
        formData.append("file", inputElement.files[0]);

        try {
          const response = await storeAuth.axiosInstance.post(
            `${server}/file/resume`,
            formData
          );
          const { message } = response.data;

          storeAlert.alertMessage.setAlert(
            "alert-success",
            "Данные успешно загружены"
          );
          dataProfile.value.candId = message;
          router.push({ name: "profile", params: { id: message } });
          this.getResume();
        } catch (error) {
          console.error(error);
        }
      } else {
        storeAlert.alertMessage.setAlert(
          "alert-warning",
          "Ошибка при загрузке файла"
        );
      }
    },

    deleteResume: async function (): Promise<void> {
      if (
        ["robot", "finish"].includes(
          classifyApp.classData.status[this.resume["status_id"]]
        )
      ) {
        storeAlert.alertMessage.setAlert(
          "alert-warning",
          "Нельзя удалить запись с текущим статусом"
        );
        return;
      }

      if (confirm(`Вы действительно хотите удалить анкету?`)) {
        try {
          const response = await storeAuth.axiosInstance.delete(
            `${server}/resume`
          );
          console.log(response.status);
          router.push({ name: "persons", params: { group: "staffsec" } });

          storeAlert.alertMessage.setAlert(
            "alert-info",
            `Запись с ID ${dataProfile.value.candId} удалена`
          );
        } catch (error) {
          console.error(error);
        }
      }
    },
  });

  const dataAnketa = ref({
    docums: Array<Document>(),
    addrs: Array<Address>(),
    conts: Array<Contact>(),
    works: Array<Work>(),
    relate: Array<Relation>(),
    affilation: Array<Affilation>(),
    form: <Record<string, any>>{},

    getItem: async function (item: string): Promise<void> {
      try {
        const response = await storeAuth.axiosInstance.get(
          `${server}/${dataProfile.value.item}/${dataProfile.value.candId}`
        );
        switch (item) {
          case "document":
            this.docums = response.data;
            break;
          case "address":
            this.addrs = response.data;
            break;
          case "contact":
            this.conts = response.data;
            break;
          case "workplace":
            this.works = response.data;
            break;
          case "relation":
            this.relate = response.data;
            break;
          case "affilation":
            this.affilation = response.data;
            break;
          default:
            console.log(response.data);
            break;
        }
      } catch (error) {
        console.error(error);
        storeAlert.alertMessage.setAlert(
          "alert-danger",
          `Ошибка обработки ${error}`
        );
      }
    },

    updateItem: async function (): Promise<void> {
      try {
        const response =
          dataProfile.value.action === "create"
            ? await storeAuth.axiosInstance.post(
                `${server}/${dataProfile.value.item}/${dataProfile.value.candId}`,
                this.form
              )
            : await storeAuth.axiosInstance.patch(
                `${server}/${dataProfile.value.item}/${dataProfile.value.itemId}`,
                this.form
              );

        console.log(response.status);

        storeAlert.alertMessage.setAlert(
          "alert-success",
          "Данные успешно обновлены"
        );
        this.getItem(dataProfile.value.item);
      } catch (error) {
        storeAlert.alertMessage.setAlert(
          "alert-danger",
          `Возникла ошибка ${error}`
        );
      }
      clearForm(this.form);
      dataProfile.value.item = "";
    },

    deleteItem: async function (item: string, id: string): Promise<void> {
      if (confirm(`Вы действительно хотите удалить запись?`)) {
        try {
          const response = await storeAuth.axiosInstance.delete(
            `${server}/${item}/${id}`
          );
          console.log(response.status);
          this.getItem(item);

          storeAlert.alertMessage.setAlert(
            "alert-info",
            `Запись с ID ${id} удалена`
          );
        } catch (error) {
          console.error(error);
        }
      }
    },
  });

  const dataChecks = ref({
    verification: Array<Verification>(),
    robot: Array<Robot>(),
    pfo: Array<Pfo>(),
    inquisition: Array<Inquisition>(),
    needs: Array<Needs>(),

    getItem: async function (): Promise<void> {
      if (
        dataProfile.value.item === "check" &&
        dataProfile.value.action === "add"
      ) {
        if (
          classifyApp.classData.status[dataResume.value.resume["status_id"]] ===
            "save" ||
          classifyApp.classData.status[dataResume.value.resume["status_id"]] ===
            "manual" ||
          classifyApp.classData.status[dataResume.value.resume["status_id"]] ===
            "robot"
        ) {
          storeAlert.alertMessage.setAlert(
            "alert-warning",
            "Нельзя добавить проверку к текущему статусу"
          );
          return;
        }
      }
      try {
        const response = await storeAuth.axiosInstance.get(
          `${server}/${dataProfile.value.item}/${dataProfile.value.candId}`,
          {
            params: {
              action: dataProfile.value.action,
            },
          }
        );
        switch (dataProfile.value.item) {
          case "check":
            this.verification = response.data;
            break;
          case "robot":
            this.robot = response.data;
            break;
          case "poligraf":
            this.pfo = response.data;
            break;
          case "investigation":
            this.inquisition = response.data;
            break;
          case "inquiry":
            this.needs = response.data;
            break;
          default:
            console.log(response.data);
            break;
        }
        if (
          dataProfile.value.item === "check" &&
          (dataProfile.value.action === "add" ||
            dataProfile.value.action === "self")
        ) {
          this.getItem();
        }
      } catch (error) {
        console.error(error);
        storeAlert.alertMessage.setAlert(
          "alert-danger",
          `Ошибка обработки ${error}`
        );
      }
    },

    updateItem: async function (): Promise<void> {
      try {
        const response =
          dataProfile.value.action === "create"
            ? await storeAuth.axiosInstance.post(
                `${server}/${dataProfile.value.item}/${dataProfile.value.candId}`,
                dataProfile.value.form
              )
            : await storeAuth.axiosInstance.patch(
                `${server}/${dataProfile.value.item}/${dataProfile.value.itemId}`,
                dataProfile.value.form
              );

        console.log(response.status);

        storeAlert.alertMessage.setAlert(
          "alert-success",
          "Данные успешно обновлены"
        );
        this.getItem();
      } catch (error) {
        storeAlert.alertMessage.setAlert(
          "alert-danger",
          `Возникла ошибка ${error}`
        );
      }
      clearForm(dataProfile.value.form);
      dataProfile.value.action = "";
    },

    deleteItem: async function (): Promise<void> {
      if (
        classifyApp.classData.status[dataResume.value.resume["status_id"]] ===
        "robot"
      ) {
        storeAlert.alertMessage.setAlert(
          "alert-warning",
          "Нельзя удалить запись из анкеты текущим статусом"
        );
        return;
      }
      if (confirm(`Вы действительно хотите удалить запись?`)) {
        try {
          const response = await storeAuth.axiosInstance.delete(
            `${server}/${dataProfile.value.item}${dataProfile.value.itemId}`
          );
          console.log(response.status);
          this.getItem();

          storeAlert.alertMessage.setAlert(
            "alert-info",
            `Запись с ID ${dataProfile.value.itemId} удалена`
          );
        } catch (error) {
          console.error(error);
        }
      }
    },
  });

  return { dataProfile, dataResume, dataAnketa, dataChecks };
});
