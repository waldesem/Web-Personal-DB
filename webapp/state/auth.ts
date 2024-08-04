import axios from "axios";
import { router } from "@/router";
import { stateAlert } from "@/state";

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

axiosAuth.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error: any) => {
    if (error.request.status == 401 || error.request.status == 403) {
      router.push({ name: "login" });
    } else if (error.request.status == 400) {
      stateAlert.setAlert("alert-warning", "Операция завершилась неудачно")
    } else {
      return Promise.reject(error);
    }
  }
);

