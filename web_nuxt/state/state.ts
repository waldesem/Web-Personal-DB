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

  async function getCurrentUser() {
    const response = await authFetch(`${server}/auth`);
    const data = response as Record<string, unknown>;
    if (!data) {
      return navigateTo("/login")
    };
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
    const response = await authFetch(`${server}/index/${persons.value.page}`, {
      params: {
        search: persons.value.search,
      },
    });
    [persons.value.candidates, persons.value.next, persons.value.prev] =
      response as [Persons[], boolean, boolean];

    persons.value.updated = `${new Date().toLocaleDateString(
      "ru-RU"
    )} в ${new Date().toLocaleTimeString("ru-RU")}`;
  }
  return { persons, getCandidates };
};

export const stateAnketa = () => {
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
    anketa.value[item as keyof typeof anketa.value] = (await authFetch(
      `${server}/${item}/${id}`,
      {
        params: {
          action: action,
        },
      }
    )) as never;
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
    const response = await authFetch(`${server}/region/${share.value.candId}`, {
      params: {
        region: anketa.value.persons["region"],
      },
    });
    console.log(response);
    getItem("persons");
    const toast = useToast();
    toast.add({
      icon: "i-heroicons-check-circle",
      title: "Информация",
      description: "Изменение региона успешно",
      color: "green",
    });
  }

  async function updateItem(param: string, form: object): Promise<void> {
    const response = await authFetch(
      `${server}/${param}/${share.value.candId}`,
      {
        method: "POST",
        body: form,
      }
    );
    console.log(response);
    getItem(param);
    const toast = useToast();
    toast.add({
      icon: "i-heroicons-check-circle",
      title: "Успешно",
      description: "Информация обновлена",
      color: "green",
    });
  }

  async function deleteItem(id: string, param: string): Promise<void> {
    if (!confirm(`Вы действительно хотите удалить запись?`)) return;
    const response = await authFetch(`${server}/${param}/${id}`, {
      method: "DELETE",
    });
    console.log(response);
    if (param === "persons") {
      navigateTo("/persons");
    } else getItem(param);
    const toast = useToast();
    toast.add({
      icon: "i-heroicons-information-circle",
      title: "Информация",
      description: `Запись с ID ${id} удалена`,
      color: "primary",
    });
  }

  async function submitFile(
    fileList: FileList,
    param: string,
    itemId: string
  ): Promise<void> {
    const toast = useToast();
    const formData = new FormData();
    if (fileList) {
      for (const file of fileList) {
        if (param === "image" && file.size > 1024 * 1024) {
          toast.add({
            icon: "i-heroicons-exclamation-triangle",
            title: "Внимание",
            description: "Файл слишком большой",
            color: "red",
          });
          return;
        }
        formData.append("file", file);
      }
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
      toast.add({
        icon: "i-heroicons-check-circle",
        title: "Информация",
        description: `Файлы успешно загружены`,
        color: "green",
      });
    } else {
      toast.add({
        icon: "i-heroicons-exclamation-triangle",
        title: "Внимание",
        description: "Ошибка при загрузке файла",
        color: "red",
      });
    }
  }

  async function submitResume(action: string, form: object): Promise<void> {
    if (action == "create") {
      const response = await authFetch(`${server}/resume`, {
        method: "POST",
        body: form,
      });
      console.log(response);
      const toast = useToast();
      toast.add({
        icon: "i-heroicons-check-circle",
        title: "Информация",
        description: `Данные успешно добавлены`,
        color: "green",
      });
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
