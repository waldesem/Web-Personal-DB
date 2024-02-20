import { ref } from "vue";
import { defineStore } from "pinia";
import { authStore } from "@/store/token";
import { alertStore } from "@store/alert";
import { classifyStore } from "@store/classify";
import { server } from "@utilities/utils";
import router from "@router/router";

export const userStore = defineStore("userStore", () => {
  const storeAlert = alertStore();
  const storeClasses = classifyStore();
  const storeAuth = authStore();

  const userData = ref({
    fullName: "",
    userName: "",
    userRoles: [],
    userGroups: [],

    getAuth: async function (): Promise<void> {
      try {
        const response = await storeAuth.axiosInstance.get(`${server}/login`);
        const { fullname, username, roles, groups } = response.data;
        this.assignUserData(fullname, username, roles, groups);

        this.hasRole("admin")
          ? router.push({ name: "users", params: { group: "admins" } })
          : router.push({
              name: "persons",
              params: { group: this.userGroups[0]["group"] },
            });
        storeClasses.classData.getClasses();
        storeAlert.alertMessage.setAlert();
      } catch (error) {
        storeAlert.alertMessage.setAlert("alert-warning", error as string);
        this.userLogout();
      }
    },

    userLogout: async function (): Promise<void> {
      try {
        const response = await storeAuth.axiosInstance.delete(
          `${server}/login`
        );
        console.log(response.data);
      } catch (error) {
        storeAlert.alertMessage.setAlert("alert-warning", error as string);
      }

      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");

      this.assignUserData();

      router.push({ name: "login" });
    },

    hasRole: function (role: string): boolean {
      return this.userRoles.some((r: { role: any }) => r.role === role);
    },

    hasGroup: function (group: string): boolean {
      return this.userGroups.some((g: { group: any }) => g.group === group);
    },

    assignUserData(name = "", user = "", roles = [], groups = []) {
      Object.assign(this, {
        fullName: name,
        userName: user,
        userRoles: roles,
        userGroups: groups,
      });
    },
  });
  return {
    userData,
  };
});
