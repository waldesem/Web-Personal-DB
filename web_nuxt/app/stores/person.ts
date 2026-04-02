import type { Person, PersonExt, PersonId } from "@/types";

export const usePersonStore = defineStore("person", () => {
  const { $api } = useNuxtApp();

  const data = ref({} as PersonExt);

  const personId = computed(() => useRoute().params.id as string);

  // Определяем функцию для получения данных из API
  async function getPerson() {
    data.value = await $api<PersonExt>("/routes/persons/" + personId.value);
  }

  // Определяем функцию для переключения режима редактирования
  async function switchStatus() {
    return await $api.raw("/routes/persons/status/" + personId.value);
  }

  async function addPerson(form: Person) {
    return await $api.raw<Partial<PersonId>>("/routes/persons", {
      method: "POST",
      body: form,
    });
  }

  async function editPerson(form: Person) {
    return await $api.raw("/routes/persons" + personId.value, {
      method: "PATCH",
      body: form,
    });
  }

  // Определяем функцию для удаления данных
  async function deletePerson() {
    return await $api.raw(`/routes/persons/${personId.value}`, {
      method: "DELETE",
    });
  }

  return {
    data,
    personId,
    getPerson,
    switchStatus,
    addPerson,
    editPerson,
    deletePerson,
  };
});
