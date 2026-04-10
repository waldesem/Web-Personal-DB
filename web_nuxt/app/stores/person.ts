import { Roles, type Person } from "@/types";

export const usePersonStore = defineStore("person", () => {
  const { $api } = useNuxtApp();

  const session = useSessionStore();

  const data = ref({} as Person);

  const personId = ref("");

  const lock = ref(true);

  const blocked = computed(() => {
    return session.user?.role !== Roles.user;
  });

  const locked = computed(() => {
    return lock.value && session.user?.id !== data.value.user_id;
  });

  // Определяем функцию для получения данных из API
  async function getPerson(id: string) {
    personId.value = id;
    data.value = await $api<Person>("/routes/persons/" + personId.value);
  }

  // Определяем функцию для переключения режима редактирования
  async function switchStatus() {
    if (locked.value) {
      if (!confirm("Анкета значится за другим пользователем. Продолжить?")) {
        return;
      }
      await $api.raw("/routes/persons/status/" + personId.value);
      await getPerson(personId.value);
    }
    lock.value = true;
  }

  async function addPerson(form: Person) {
    return await $api.raw("/routes/persons", {
      method: "POST",
      body: form,
    });
  }

  async function editPerson(form: Person) {
    return await $api.raw("/routes/persons/" + personId.value, {
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
    lock,
    locked,
    blocked,
    personId,
    getPerson,
    switchStatus,
    addPerson,
    editPerson,
    deletePerson,
  };
});
