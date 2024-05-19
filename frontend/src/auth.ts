import axios from "axios";
import { server, expiredToken } from "@/utilities";
import { router } from "@/router";

export const axiosAuth = axios.create();

axiosAuth.interceptors.request.use(
  async (config: any) => {

    const accessToken = localStorage.getItem("access_token");
    const refreshToken = localStorage.getItem("refresh_token");

    if (!expiredToken(refreshToken)) {
      if (expiredToken(accessToken)) {
        try {
          const response = await axios.post(`${server}/auth/refresh`, null, {
            headers: {
              Authorization: `Bearer ${refreshToken}`,
            },
          });
          const { access_token } = response.data;
          localStorage.setItem("access_token", access_token);
        } catch (error) {
          router.push({ name: "login" });
          return Promise.reject(error);
        }
      }
    } else {
      router.push({ name: "login" });
      return Promise.reject("Refresh token not available or expired");
    }
    config.headers["Authorization"] = `Bearer ${accessToken}`;
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);
