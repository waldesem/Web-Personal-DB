import type { Items } from "@/types";

export const useItemStore = defineStore("items", () => {
  const { $api } = useNuxtApp();

  const person = usePersonStore();

  const items = ref<Items>({} as Items);

  async function getItems() {
    items.value = await $api<Items>("/routes/items/" + person.personId);
  }

  // Определяем функцию для получения данных из API
  async function getItem(view: keyof Items) {
    items.value[view] = await $api(`/routes/items/${view}/${person.personId}`);
  }

  async function addItem(view: keyof Items, form: object) {
    return await $api.raw(`/routes/items/${view}/${person.personId}`, {
      method: "POST",
      body: { ...form, item: view }, // add discriminator for backend validation
    });
  }

  async function editItem(view: keyof Items, itemId: string, form: object) {
    return await $api.raw(
      `/routes/items/${view}/${person.personId}/${itemId}`,
      {
        method: "PATCH",
        body: { ...form, item: view }, // add discriminator for backend validation
      },
    );
  }

  // Определяем функцию для удаления данных
  async function deleteItem(view: keyof Items, itemId: string) {
    return await $api.raw(
      `/routes/items/${view}/${person.personId}/${itemId}`,
      {
        method: "DELETE",
      },
    );
  }

  return {
    items,
    getItems,
    getItem,
    addItem,
    editItem,
    deleteItem,
  };
});
