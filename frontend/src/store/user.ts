import { defineStore } from "pinia";
import { ref } from "vue";
import { authStore } from "@/store/auth";
import { alertStore } from "../store/alert";
import { server } from "@utilities/utils";
import { router } from "../router/router";

export const userStore = defineStore("userStore", () => {
  const storeAuth = authStore();
  const storeAlert = alertStore();

  const userData = ref({
    userId: "",
    fullName: "",
    userName: "",
    userRoles: [],
    hasAdmin: false,

    getAuth: async function (): Promise<void> {
      try {
        const response = await storeAuth.axiosInstance.get(`${server}/login`);
        const { id, fullname, username, roles } = response.data;

        Object.assign(this, {
          userId: id,
          fullName: fullname,
          userName: username,
          userRoles: roles,
        });

        this.userRoles.some((r: { role: any }) => r.role === "admin")
          ? router.push({ name: "users" })
          : router.push({ name: "persons" });
        storeAlert.alertMessage.setAlert();
      } catch (error) {
        storeAlert.alertMessage.setAlert("alert-warning", error as string);
      }
    },
  });

  return {
    userData,
  };
});
