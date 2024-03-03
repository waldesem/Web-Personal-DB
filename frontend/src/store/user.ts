import { defineStore } from "pinia";
import { ref } from "vue";

export const userStore = defineStore("userStore", () => {

  const userData = ref({
    userId: "",
    fullName: "",
    userName: "",
    userRoles: [],
    hasAdmin: false,
  });
  return {
    userData,
  };
});
