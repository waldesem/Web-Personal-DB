import axios from "axios";
import { ref } from "vue";
import { useRouter } from "vue-router";
import { defineStore } from "pinia";
import { alertStore } from "@store/alert";
import { classifyStore } from "@store/classify";
import { server } from "@utilities/utils";

export const authStore = defineStore("authStore", () => {
  const router = useRouter();

  const storeAlert = alertStore();
  const storeClasses = classifyStore();

  const axiosInstance = ref(axios.create());

  const refreshToken = ref("");
  const accessToken = ref("");

  axiosInstance.value.interceptors.request.use(
    async (config) => {
      if (!refreshToken.value) {
        router.push({ name: "login" });
        return Promise.reject("Refresh token not available");
      }

      const expiry_refresh = JSON.parse(
        atob(refreshToken.value.split(".")[1])
      ).exp;
      if (Math.floor(new Date().getTime() / 1000) >= expiry_refresh) {
        router.push({ name: "login" });
        return Promise.reject("Refresh token expired");
      }

      if (!accessToken.value) {
        router.push({ name: "login" });
        return Promise.reject("Access token not available");
      }

      const expiry_access = JSON.parse(
        atob(accessToken.value.split(".")[1])
      ).exp;
      if (Math.floor(new Date().getTime() / 1000) >= expiry_access) {
        try {
          const response = await axios.post(`${server}/refresh`, null, {
            headers: {
              Authorization: `Bearer ${refreshToken.value}`,
            },
          });
          const { access_token } = response.data;

          if (!access_token) {
            router.push({ name: "login" });
            return Promise.reject("Access token not available");
          }
          accessToken.value = access_token;
        } catch (error) {
          router.push({ name: "login" });
          return Promise.reject(error);
        }
      }
      config.headers["Authorization"] = `Bearer ${accessToken.value}`;
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

  const userData = ref({
    userId: "",
    fullName: "",
    userName: "",
    userRoles: [],
    hasAdmin: false,

    getAuth: async function (): Promise<void> {
      try {
        const response = await axiosInstance.value.get(`${server}/login`);
        const { id, fullname, username, roles } = response.data;
        Object.assign(this, {
          userId: id,
          fullName: fullname,
          userName: username,
          userRoles: roles,
        });

        this.hasRole("admin")
          ? router.push({ name: "admin" })
          : router.push({ name: "staffsec" });
        storeClasses.classData.getClasses();
        storeAlert.alertMessage.setAlert();
      } catch (error) {
        storeAlert.alertMessage.setAlert("alert-warning", error as string);
        this.userLogout();
      }
    },

    userLogout: async function (): Promise<void> {
      try {
        const response = await axiosInstance.value.delete(`${server}/login`);
        console.log(response.status);
      } catch (error) {
        storeAlert.alertMessage.setAlert("alert-warning", error as string);
      }

      accessToken.value = "";
      refreshToken.value = "";

      router.push({ name: "login" });
    },

    hasRole: function (role: string): boolean {
      return this.userRoles.some((r: { role: any }) => r.role === role);
    },
  });

  return {
    axiosInstance,
    accessToken,
    refreshToken,
    userData,
  };
});
