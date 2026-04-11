import type { Session } from "@/types";

export const useSessionStore = defineStore("session", {
  state: () => ({
    user: {} as Session,
  }),

  actions: {
    async getUser() {
      const { $api } = useNuxtApp();
      this.user = await $api<Session>("/routes/auth/session");
    },
  },
});
