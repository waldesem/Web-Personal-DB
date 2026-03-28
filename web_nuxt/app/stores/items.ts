import type { Items } from "@/types";

export const useItemStore = defineStore("items", () => {
  const { $api } = useNuxtApp();

  const personStore = usePersonStore();

  const items = ref<Items>({} as Items);

  async function getItems() {
    try {
      items.value = await $api<Items>("/routes/items/" + personStore.person.id);
    } catch (error) {
      console.error(error);
    }
  }

  // Определяем функцию для получения данных из API
  async function getItem(view: keyof Items) {
    try {
      items.value[view] = await $api(
        `/routes/items/${view}/${personStore.person.id}`,
      );
    } catch (error) {
      console.error(error);
    }
  }

  async function addItem(view: keyof Items, form: object) {
    try {
      return await $api.raw(`/routes/items/${view}/${personStore.person.id}`, {
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
        `/routes/items/${view}/${personStore.person.id}/${itemId}`,
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
        `/routes/items/${view}/${personStore.person.id}/${itemId}`,
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
