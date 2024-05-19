import axios from "axios";
import { server, expiredToken } from "@/utilities";
import { router } from "@/router";

export const axiosAuth = axios.create();

axiosAuth.interceptors.request.use(
  async (config: any) => {
    // Check if refresh token is expired
    const refreshToken = localStorage.getItem("refresh_token");
    if (expiredToken(refreshToken)) {
      router.push({ name: "login" });
      return Promise.reject("Refresh token not available or expired");
    }

    // Check if access token is expired
    if (expiredToken(localStorage.getItem("access_token"))) {
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

    // Set access token in request header
    config.headers["Authorization"] = `Bearer ${localStorage.getItem(
      "access_token"
    )}`;
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);
