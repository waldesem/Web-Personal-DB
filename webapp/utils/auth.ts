import axios from "axios";

export const axiosAuth = axios.create();

axiosAuth.interceptors.request.use(
  async (config: any) => {
    const user_token = localStorage.getItem("user_token");
    if (user_token) {
      config.headers["Authorization"] = `Basic ${user_token}`;
      return config;
    } 
    return navigateTo("/login");
  },
  (error) => {
    return Promise.reject(error);
  }
);

axiosAuth.interceptors.response.use(
  (response) => {
    return response;
  },
  (error: any) => {
    return Promise.reject(error);
  }
);

