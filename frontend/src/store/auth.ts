import axios from "axios";
import { ref } from "vue";
import { useRouter } from "vue-router";
import { defineStore } from "pinia";
import { server } from "@utilities/utils";

export const authStore = defineStore("authStore", () => {
  const router = useRouter();

  const axiosInstance = ref(axios.create());

  const refreshToken = ref(localStorage.getItem("refresh_token"));
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
  return {
    axiosInstance,
    accessToken,
    refreshToken,
  };
});
