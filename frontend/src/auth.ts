import axios from "axios";
import { router } from "@/router";

export const axiosAuth = axios.create();

axiosAuth.interceptors.request.use(
  async (config: any) => {
    const user_token = localStorage.getItem("user_token");
    if (user_token) {
      config.headers["Authorization"] = `Basic ${user_token}`;
      return config;
    } else {
      router.push({ name: "login" });
      return Promise.reject("Token not available");
    }
  },
  (error) => {
    return Promise.reject(error);
  }
);
