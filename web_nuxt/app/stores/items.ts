import type { Items } from "@/types";

export const useItemStore = defineStore("items", () => {
  const { $api } = useNuxtApp();

  const person = usePersonStore();

  const items = ref<Items>({} as Items);

  async function getItems() {
    try {
      items.value = await $api<Items>("/routes/items/" + person.personId);
    } catch (error) {
      console.error(error);
    }
  }

  // Определяем функцию для получения данных из API
  async function getItem(view: keyof Items) {
    try {
      items.value[view] = await $api(
        `/routes/items/${view}/${person.personId}`,
      );
    } catch (error) {
      console.error(error);
    }
  }

  async function addItem(view: keyof Items, form: object) {
    try {
      return await $api.raw(`/routes/items/${view}/${person.personId}`, {
        method: "POST",
        body: { ...form, item: view }, // add discriminator for backend validation
      });
    } catch (error) {
      console.error(error);
    }
  }

  async function editItem(view: keyof Items, itemId: string, form: object) {
    try {
      return await $api.raw(
        `/routes/items/${view}/${person.personId}/${itemId}`,
        {
          method: "PATCH",
          body: { ...form, item: view }, // add discriminator for backend validation
        },
      );
    } catch (error) {
      console.error(error);
    }
  }

  // Определяем функцию для удаления данных
  async function deleteItem(view: keyof Items, itemId: string) {
    try {
      return await $api.raw(
        `/routes/items/${view}/${person.personId}/${itemId}`,
        {
          method: "DELETE",
        },
      );
    } catch (error) {
      console.error(error);
    }
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
