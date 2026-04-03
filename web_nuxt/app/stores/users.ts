import type { Actions, Roles, User, UserForm } from "@/types";

export const useUserStore = defineStore("users", () => {
  const { $api } = useNuxtApp();

  const session = useSessionStore();

  const data = ref([] as User[]);

  async function getUsers() {
    data.value = await $api("/routes/users");
  }

  async function submitUser(form: UserForm) {
    return await $api.raw("/routes/user", {
      method: "POST",
      body: form,
    });
  }

  async function editUser(item: Actions | Roles, user_id: string) {
    if (user_id === session.user?.id) return;
    return await $api.raw("/routes/user/" + user_id, {
      method: "POST",
      body: { item: item },
    });
  }

  return {
    data,
    getUsers,
    editUser,
    submitUser,
  };
});
