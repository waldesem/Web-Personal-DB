import { stateUser, server } from "@/state/state";
import { axiosAuth } from "@/utils/auth";

export default defineNuxtRouteMiddleware(async (to, from) => {
  const userState = stateUser();

  if (to.name != "login" && !userState.user.value.auth) {
    
    try {
      const auth = await axiosAuth.get(`${server}/auth`);
      const user = auth.data;
      Object.assign(userState.user.value, {
        auth: true,
        userId: user["id"],
        username: user["username"],
        role: user["role"],
        region: user["region"],
      });
      return navigateTo("/persons");
    } catch (error: any) {
      console.error(error);
      return navigateTo("/login");
    }
  }
})