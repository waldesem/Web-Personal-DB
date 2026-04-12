import type { Session } from "@/types";

export const useSessionStore = defineStore("session", () => {
  const user = ref({} as Session);

  async function getUser() {
    const { $api } = useNuxtApp();
    user.value = await $api<Session>("/routes/auth/session");
  }

  function $reset() {
    user.value = {} as Session;
  }

  return { user, getUser, $reset };
});
