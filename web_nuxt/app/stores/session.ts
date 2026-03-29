import type { Session } from "@/types";

export const useSessionStore = defineStore("session", () => {
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
