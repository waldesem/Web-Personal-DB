import type { Session } from "@/types";

export const useUserStore = defineStore("user", () => {
  const { $api } = useNuxtApp();

  const user = ref<Session>();

  async function getUser() {
    user.value = await $api<Session>("/routes/auth/session");
  }

  return {
    user,
    getUser,
  };
});
