import { useFetchAuth } from "../utils/auth";
import type { Classes, Profile } from "@/utils/interfaces";

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

  async function updateItem(param: string, form: object): Promise<void> {
    const response = await authFetch(
      `${server}/${param}/${share.value.candId}`,
      {
        method: "POST",
        body: form,
      }
    );
    console.log(response);
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
        formData.append("file", file);
      }
      const response = await authFetch(`${server}/file/${param}/${itemId}`, {
        method: "POST",
        body: formData,
      });
      console.log(response);
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
    formData.delete("file");
  }

  return {
    anketa,
    share,
    getItem,
    updateItem,
    deleteItem,
    submitFile,
  };
};
