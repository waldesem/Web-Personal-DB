import type { Person, PersonExt, PersonId } from "@/types";

export const usePersonStore = defineStore("person", () => {
  const { $api } = useNuxtApp();

  const person = ref({} as PersonExt);

  // Определяем функцию для получения данных из API
  async function getPerson() {
    try {
      person.value = await $api<PersonExt>(
        "/routes/persons/" + person.value?.id,
      );
    } catch (error) {
      console.error(error);
    }
  }

  // Определяем функцию для переключения режима редактирования
  async function switchStatus() {
    try {
      return await $api.raw("/routes/persons/status/" + person.value?.id);
    } catch (error) {
      console.error(error);
    }
  }

  async function addPerson(form: Person) {
    return await $api.raw<Partial<PersonId>>("/routes/persons", {
      method: "POST",
      body: form,
    });
  }

  async function editPerson(form: Person) {
    return await $api.raw<Partial<PersonId>>(
      "/routes/persons" + person.value?.id,
      {
        method: "PATCH",
        body: form,
      },
    );
  }

  // Определяем функцию для удаления данных
  async function deletePerson() {
    try {
      return await $api.raw(`/routes/persons/${person.value?.id}`, {
        method: "DELETE",
      });
    } catch (error) {
      console.error(error);
    }
  }

  return {
    person,
    getPerson,
    switchStatus,
    addPerson,
    editPerson,
    deletePerson,
  };
});
