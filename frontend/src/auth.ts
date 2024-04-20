import axios from "axios";
import { useRouter } from "vue-router";
import { server, readToken } from "@/utilities";
import { stateToken } from "@/state";

const router = useRouter();

export const axiosInstance = axios.create();

axiosInstance.interceptors.request.use(
  async (config: any) => {
    stateToken.refreshToken = localStorage.getItem("refresh_token");

    if (!stateToken.refreshToken) {
      router.push({ name: "login" });
      return "Refresh token not available";
    }

    if (
      Math.floor(new Date().getTime() / 1000) >=
      readToken(stateToken.refreshToken, "exp")
    ) {
      router.push({ name: "login" });
      return Promise.reject("Refresh token expired");
    }

    if (
      !stateToken.accessToken ||
      Math.floor(new Date().getTime() / 1000) >=
        readToken(stateToken.accessToken, "exp")
    ) {
      try {
        const response = await axios.post(`${server}/refresh`, null, {
          headers: {
            Authorization: `Bearer ${stateToken.refreshToken}`,
          },
        });
        const { access_token } = response.data;

        if (!access_token) {
          router.push({ name: "login" });
          return Promise.reject("Access token not available");
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
