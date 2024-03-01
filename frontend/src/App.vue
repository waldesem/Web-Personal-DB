<script setup lang="ts">
import { onBeforeMount, ref, provide } from "vue";
import { authStore } from "@/store/auth";
import { alertStore } from "./store/alert";
import { classifyStore } from "./store/classify";
import { server } from "@utilities/utils";
import { router } from "./router/router";

const storeAuth = authStore();
const storeAlert = alertStore();
const storeClasses = classifyStore();

onBeforeMount(async () => {
  await userData.value.getAuth();
});


const userData = ref({
  userId: "",
  fullName: "",
  userName: "",
  userRoles: [],
  hasAdmin: false,

  getAuth: async function (): Promise<void> {
    try {
      const response = await storeAuth.axiosInstance.get(`${server}/login`);
      const { id, fullname, username, roles } = response.data;
      Object.assign(this, {
        userId: id,
        fullName: fullname,
        userName: username,
        userRoles: roles,
      });

      this.userRoles.some((r: { role: any }) => r.role === "admin")
        ? router.push({ name: "admin" })
        : router.push({ name: "staffsec" });
      storeClasses.classData.getClasses();
      storeAlert.alertMessage.setAlert();
    } catch (error) {
      storeAlert.alertMessage.setAlert("alert-warning", error as string);
    }
  },
});

provide("fullName", userData.value.fullName);
provide("hasAdmin", userData.value.hasAdmin);
</script>

<template>
  <RouterView />
</template>

<style>
html,
body {
  scrollbar-gutter: stable;
}
</style>
