import { useFetchAuth } from "../utils/auth";
import type { Classes, Profile, User } from "@/types/interfaces";
import { Buffer } from 'buffer';

const authFetch = useFetchAuth();

export const server = "/api";

export const userToken = ref("");

export const stateUser = () => {
  if (!userToken.value) {
    return {} as Ref<User>;
  }
  const payload = userToken.value.split(" ")[1];
  const user = useState("user", () => (
    JSON.parse(
      Buffer.from(payload.split(".")[1], "base64").toString()
    ) as User
  ));
  return user as Ref<User>;
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
  }));

  async function getItem(
    item: string,
    id: string = share.value.candId
  ): Promise<void> {
    anketa.value[item as keyof typeof anketa.value] = (await authFetch(
      `${server}/${item}/${id}`
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
