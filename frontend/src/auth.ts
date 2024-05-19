import axios from "axios";
import { server, expiredToken } from "@/utilities";
import { router } from "@/router";
import { stateToken } from "@/state";

export const axiosAuth = axios.create();

axiosAuth.interceptors.request.use(
  async (config: any) => {
    if (expiredToken(stateToken.tokens.refreshToken)) {
      router.push({ name: "login" });
      return Promise.reject("Refresh token not available or expired");
    } else {
      if (expiredToken(stateToken.tokens.accessToken)) {
        try {
          const response = await axios.post(`${server}/auth/refresh`, null, {
            headers: {
              Authorization: `Bearer ${stateToken.tokens.refreshToken}`,
            },
          });
          const { access_token } = response.data;
          stateToken.setTokens(access_token, stateToken.tokens.refreshToken);
        } catch (error) {
          router.push({ name: "login" });
          return Promise.reject(error);
        }
      }
    }
    config.headers["Authorization"] = `Bearer ${stateToken.tokens.accessToken}`;
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);
