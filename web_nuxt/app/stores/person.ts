import type { Person, PersonExt, PersonId } from "@/types";

export const usePersonStore = defineStore("person", () => {
  const { $api } = useNuxtApp();

  const person = ref({} as PersonExt);

  const personId = computed(() => useRoute().params.id as string);

  // Определяем функцию для получения данных из API
  async function getPerson() {
    try {
      person.value = await $api<PersonExt>("/routes/persons/" + personId.value);
    } catch (error) {
      console.error(error);
    }
  }

  // Определяем функцию для переключения режима редактирования
  async function switchStatus() {
    try {
      return await $api.raw("/routes/persons/status/" + personId.value);
    } catch (error) {
      console.error(error);
    }
  }

  async function addPerson(form: Person) {
    try {
      return await $api.raw<Partial<PersonId>>("/routes/persons", {
        method: "POST",
        body: form,
      });
    } catch (error) {
      console.error(error);
    }
  }

  async function editPerson(form: Person) {
    try {
      return await $api.raw<Partial<PersonId>>(
        "/routes/persons" + personId.value,
        {
          method: "PATCH",
          body: form,
        },
      );
    } catch (error) {
      console.error(error);
    }
  }

  // Определяем функцию для удаления данных
  async function deletePerson() {
    try {
      return await $api.raw(`/routes/persons/${personId.value}`, {
        method: "DELETE",
      });
    } catch (error) {
      console.error(error);
    }
  }

  return {
    person,
    personId,
    getPerson,
    switchStatus,
    addPerson,
    editPerson,
    deletePerson,
  };
});
