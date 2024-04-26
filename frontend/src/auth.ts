import axios from "axios";
import { server, expiredToken } from "@/utilities";
import { router } from "@/router";
import { stateToken } from "@/state";

export const axiosAuth = axios.create();

axiosAuth.interceptors.request.use(
  async (config: any) => {

    stateToken.refreshToken = localStorage.getItem("refresh_token");

    if (expiredToken(stateToken.refreshToken)) {
      router.push({ name: "login" });
      return Promise.reject("Refresh token not available or expired");
    }

    if (expiredToken(stateToken.refreshToken)) {
      try {
        const response = await axios.post(`${server}/refresh`, null, {
          headers: {
            Authorization: `Bearer ${stateToken.refreshToken}`,
          },
        });
        const { access_token } = response.data;

        if (!access_token) {
          router.push({ name: "login" });
          return Promise.reject("Access token not available or expired");
        }
        stateToken.accessToken = access_token;
      } catch (error) {
        router.push({ name: "login" });
        return Promise.reject(error);
      }
    }
    config.headers["Authorization"] = `Bearer ${stateToken.accessToken}`;
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);
