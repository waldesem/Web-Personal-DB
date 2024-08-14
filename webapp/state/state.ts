import { useFetchAuth } from "../utils/auth";
import type { Classes, Persons, Profile } from "@/utils/interfaces";

const authFetch = useFetchAuth();

export const server = "/api";
export const userToken = ref("");

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
      const response = await authFetch(`${server}/auth`);
      const data = response as Record<string, unknown>;
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
    } catch (error: unknown) {
      console.error(error);
      navigateTo("/login");
    }
  }
  return { user, getCurrentUser };
};

export const stateClassify = () => {
  const classes = useState(`${server}/classes`, () => ({} as Classes));

  async function getClassify(): Promise<void> {
    classes.value = await $fetch(`${server}/classes`);
  }
  return { classes, getClassify };
};

export const stateAlert = () => {
  const alertMessage = useState("alertMessage", () => ({
    attr: "red",
    title: "Внимание!",
    text: "Обнаружена ошибка. Пожалуйста, обратитесь к разработчику.",
    show: false,
    timeOut: 0,
  }));

  function setAlert(attr: string, title: string, text: string) {
    window.clearTimeout(alertMessage.value.timeOut);
    Object.assign(alertMessage.value, {
      show: true,
      attr: attr,
      title: title,
      text: text,
      timeOut: window.setTimeout(() => {
        alertMessage.value.show = false;
      }, 6000),
    });
  }
  return { alertMessage, setAlert };
};

export const statePersons = () => {
  const persons = useState(`${server}/persons`, () => ({
    candidates: [] as Persons[],
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
        response as [Persons[], boolean, boolean];

      persons.value.updated = `${new Date().toLocaleDateString(
        "ru-RU"
      )} в ${new Date().toLocaleTimeString("ru-RU")}`;
    } catch (error: unknown) {
      console.error(error);
    }
  }
  return { persons, getCandidates };
};

export const stateAnketa = () => {
  const alertState = stateAlert();
  const anketa = useState("anketa", () => ({} as Profile));
  const share = useState("share", () => ({
    candId: "" as string,
    imageUrl: "" as string,
  }));

  async function getItem(
    item: string,
    action = "view",
    id: string = share.value.candId
  ): Promise<void> {
    if (
      action === "self" &&
      !confirm("Вы действительно хотите включить/выключить режим правки")
    ) {
      return;
    }
    try {
      const response = await authFetch(`${server}/${item}/${id}`, {
        params: {
          action: action,
        },
      });
      anketa.value[item as keyof typeof anketa.value] = response as any;
    } catch (error: unknown) {
      console.error(error);
      alertState.setAlert("rose", "Внимание", "Возникла ошибка");
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
    } catch (error: unknown) {
      console.error(error);
    }
  }

  async function updateItem(param: string, form: object): Promise<void> {
    try {
      const response = await authFetch(
        `${server}/${param}/${share.value.candId}`,
        {
          method: "POST",
          body: form,
        }
      );
      console.log(response);
      getItem(param);
    } catch (error: unknown) {
      console.error(error);
      alertState.setAlert("rose", "Внимание", "Произошла ошибка");
    }
  }

  async function deleteItem(id: string, param: string): Promise<void> {
    if (!confirm(`Вы действительно хотите удалить запись?`)) return;
    try {
      const response = await authFetch(`${server}/${param}/${id}`, {
        method: "DELETE",
      });
      console.log(response);
      if (param === "persons") {
        navigateTo("/persons");
      } else getItem(param);
      alertState.setAlert("primary", "Информация", `Запись с ID ${id} удалена`);
    } catch (error: unknown) {
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
      for (const file of inputElement.files) {
        if (file.size < 1024 * 1024 * 2) {
          formData.append("file", file);
        }
      }
      try {
        const response = await authFetch(`${server}/file/${param}/${itemId}`, {
          method: "POST",
          body: formData,
        });
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
          "green",
          "Успешно",
          "Файл или файлы успешно загружены"
        );
      } catch (error: unknown) {
        console.error(error);
      }
    } else {
      alertState.setAlert("rose", "Внимание", "Ошибка при загрузке файла");
    }
  }

  async function submitResume(action: string, form: object): Promise<void> {
    if (action == "create") {
      try {
        const response = await authFetch(`${server}/resume`, {
          method: "POST",
          body: form,
        });
        const person_id = response as string;
        navigateTo(`/profile/${person_id}`);
        alertState.setAlert("green", "Успешно", "Данные успешно добавлены");
      } catch (error) {
        alertState.setAlert("rose", "Внимание", `Возникла ошибка ${error}`);
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
