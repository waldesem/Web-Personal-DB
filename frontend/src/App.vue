<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount } from "vue";
import { classifyStore } from "./store/classify";
import { userStore } from "./store/user";
import { authStore } from "@/store/auth";
import { alertStore } from "@/store/alert";
import { server } from "@utilities/utils";
import { router } from "./router/router";

const FooterDiv = defineAsyncComponent(
  () => import("@components/layouts/FooterDiv.vue")
);

const storeClasses = classifyStore();
const storeUser = userStore();
const storeAuth = authStore();
const storeAlert = alertStore();

onBeforeMount(async () => {
  await getAuth();
  await storeClasses.classData.getClasses();
});

async function getAuth(): Promise<void> {
  try {
    const response = await storeAuth.axiosInstance.get(`${server}/login`);
    const { id, fullname, username, roles } = response.data;

    Object.assign(storeUser.userData, {
      userId: id,
      fullName: fullname,
      userName: username,
      userRoles: roles,
      hasAdmin: roles.some((r: { role: any }) => r.role === "admin"),
    });
    
    router.push({ name: "persons" });
    storeAlert.alertMessage.setAlert();

  } catch (error) {
    storeAlert.alertMessage.setAlert("alert-warning", error as string);
  }
};
</script>

<template>
  <RouterView />
  <FooterDiv />
</template>

<style>
html,
body {
  scrollbar-gutter: stable;
}
</style>
