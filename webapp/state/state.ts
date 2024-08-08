import { useFetchAuth } from "../utils/auth";
import * as interfaces from "../utils/interfaces";

export const server = "/api";

export const stateUser = () => {
  const user = useState("user", () => ({
    auth: false,
    userId: "",
    username: "",
    role: "",
    region: "",
  }));

  async function getCurrentUser(): Promise<void> {
    try {
      const authFetch = useFetchAuth();
      const response = authFetch(`${server}/auth`);
      const data = (await response) as Record<string, any>;
      Object.assign(user.value, {
        auth: true,
        userId: data["id"],
        username: data["username"],
        role: data["role"],
        region: data["region"],
      });
      const classifyState = stateClassify();
      await classifyState.getClassify();
      navigateTo("/persons");
    } catch (error: any) {
      console.error(error);
      navigateTo("/login");
    }
  }
  return { user, getCurrentUser };
};

export const stateClassify = () => {
  const classes = useState(`${server}/classes`, () => ({
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
  }));

  async function getClassify(): Promise<void> {
    const data = await $fetch(`${server}/classes`);
    const resp = data as Record<string, any>;
    const classifyKeys = Object.keys(classes.value);
    for (let i = 0; i < classifyKeys.length; i++) {
      classes.value[classifyKeys[i] as keyof typeof classes.value] = resp[i];
    }
  }
  return { classes, getClassify };
};

export const stateAlert = () => {
  const alertMessage = useState("alertMessage", () => ({
    attr: "",
    text: "",
    show: false,
    timeOut: 0,
  }));

  function setAlert(attr: string, text: string) {
    window.clearTimeout(alertMessage.value.timeOut);
    Object.assign(alertMessage.value, {
      show: true,
      attr: attr,
      text: text,
      timeOut: window.setTimeout(() => {
        alertMessage.value.show = false;
      }, 10000),
    });
  }
  return { alertMessage, setAlert };
};

export const statePersons = () => {
  const persons = useState(`${server}/persons`, () => ({
    candidates: <interfaces.Persons[]>[],
    page: 1,
    prev: false,
    next: true,
    search: "",
    updated: `${new Date().toLocaleDateString(
      "ru-RU"
    )} в ${new Date().toLocaleTimeString("ru-RU")}`,
  }));

  async function getCandidates(page = 1): Promise<void> {
    if (persons.value.page < 1) {
      persons.value.page = 1;
      return;
    } else {
      persons.value.page = page;
    }
    const authFetch = useFetchAuth();
    try {
      const response = await authFetch(
        `${server}/index/${persons.value.page}`,
        {
          params: {
            search: persons.value.search,
          },
        }
      );
      [persons.value.candidates, persons.value.next, persons.value.prev] =
        response as [interfaces.Persons[], boolean, boolean];

      persons.value.updated = `${new Date().toLocaleDateString(
        "ru-RU"
      )} в ${new Date().toLocaleTimeString("ru-RU")}`;
    } catch (error: any) {
      console.error(error);
    }
  }
  return { persons, getCandidates };
};

export const stateAnketa = () => {
  const alertState = stateAlert();
  const anketa = useState("anketa", () => ({
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
  }));

  const share = useState("share", () => ({
    candId: "" as string,
    imageUrl: "" as string,
  }));

  async function getItem(item: string, action = "view"): Promise<void> {
    if (
      action === "self" &&
      !confirm("Вы действительно хотите включить/выключить режим правки")
    ) {
      return;
    }
    try {
      const authFetch = useFetchAuth();
      const response = await authFetch(
        `${server}/${item}/${share.value.candId}`,
        {
          params: {
            action: action,
          },
        }
      );
      anketa.value[item as keyof typeof anketa.value] = response as any;
      if (action === "self") {
        alertState.setAlert("alert-info", "Режим проверки включен/отключен");
      }
    } catch (error: any) {
      console.error(error);
    }
  }

  async function getImage() {
    const image: Blob = await $fetch(`${server}/image`, {
      params: {
        image: anketa.value.persons.destination,
      },
      responseType: "blob",
    });
    share.value.imageUrl = window.URL.createObjectURL(new Blob([image]));
  }

  async function changeRegion(): Promise<void> {
    if (!confirm("Вы действительно хотите изменить регион?")) return;
    try {
      const authFetch = useFetchAuth();
      const response = await authFetch(
        `${server}/region/${share.value.candId}`,
        {
          params: {
            region: anketa.value.persons["region"],
          },
        }
      );
      console.log(response);
      getItem("persons");
    } catch (error: any) {
      console.error(error);
    }
  }

  async function updateItem(param: string, form: Object): Promise<void> {
    try {
      const authFetch = useFetchAuth();
      const response = await authFetch(
        `${server}/${param}/${share.value.candId}`, {
          method: "POST",
          body: form,
        }
      );
      console.log(response);
      getItem(param);
      alertState.setAlert("alert-success", "Запись успешно добавлена");
    } catch (error: any) {
      console.error(error);
    }
  }

  async function deleteItem(id: string, param: string): Promise<void> {
    if (!confirm(`Вы действительно хотите удалить запись?`)) return;
    try {
      const authFetch = useFetchAuth();
      const response = await authFetch(`${server}/${param}/${id}`, {
        method: "DELETE",
      });
      console.log(response);
      param === "persons" ? navigateTo("/persons") : getItem(param);
      alertState.setAlert("alert-info", `Запись с ID ${id} удалена`);
    } catch (error: any) {
      console.error(error);
    }
  }

  async function submitFile(
    event: Event,
    param: string,
    itemId: string
  ): Promise<void> {
    const formData = new FormData();
    const inputElement = event.target as HTMLInputElement;
    if (inputElement && inputElement.files) {
      for (let file of inputElement.files) {
        if (file.size < 1024 * 1024 * 2) {
          formData.append("file", file);
        }
      }
      try {
        const authFetch = useFetchAuth();
        const response = await authFetch(
          `${server}/file/${param}/${itemId}`, {
            method: "POST",
            body: formData,
          }
        );
        console.log(response);
        if (param === "persons") {
          const personsState = statePersons();
          personsState.getCandidates(1);
        } else if (param === "image") {
          getImage();
        } else if (param === "anketa") {
          getItem("persons");
        } else getItem(param);

        alertState.setAlert(
          "alert-success",
          "Файл или файлы успешно загружены"
        );
      } catch (error: any) {
        console.error(error);
      }
    } else {
      alertState.setAlert("alert-warning", "Ошибка при загрузке файла");
    }
  }

  async function submitResume(action: string, form: Object): Promise<void> {
    if (action == "create") {
      try {
        const authFetch = useFetchAuth();
        const response = await authFetch(`${server}/resume`, {
          method: "POST",
          body: form,
        });
        const person_id = response as string;
        navigateTo({ name: "profile", params: { id: person_id } });
        alertState.setAlert("alert-success", "Данные успешно добавлены");
      } catch (error) {
        alertState.setAlert("alert-danger", `Возникла ошибка ${error}`);
      }
    } else {
      updateItem("persons", form);
    }
  }

  return {
    anketa,
    share,
    getItem,
    changeRegion,
    updateItem,
    deleteItem,
    submitFile,
    submitResume,
    getImage,
  };
};
