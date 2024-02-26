<script setup lang="ts">
import { onBeforeMount, watch, ref, provide } from "vue";
import { defineAsyncComponent } from "vue";
import { useRoute } from "vue-router";
import { authStore } from "@/store/token";
import { alertStore } from "@store/alert";
import { classifyStore } from "@store/classify";
import { server } from "@utilities/utils";
import { router } from "@router/router";

const NavBar = defineAsyncComponent(
  () => import("@components/layouts/NavBar.vue")
);
const AlertMessage = defineAsyncComponent(
  () => import("@components/layouts/AlertMessage.vue")
);
const FooterDiv = defineAsyncComponent(
  () => import("@components/layouts/FooterDiv.vue")
);

const storeAlert = alertStore();
const storeClasses = classifyStore();
const storeAuth = authStore();
const route = useRoute();

const pageIdentity = ref("");

provide("pageIdentity", pageIdentity);

watch(
  () => route.params.group,
  (newValue) => {
    pageIdentity.value = newValue as string;
  },
  { immediate: true }
);

onBeforeMount(async () => {
  await userData.value.getAuth();
});

const userData = ref({
  userId: "",
  fullName: "",
  userName: "",
  userRoles: [],
  userGroups: [],

  getAuth: async function (): Promise<void> {
    try {
      const response = await storeAuth.axiosInstance.get(`${server}/login`);
      const { id, fullname, username, roles, groups } = response.data;
      Object.assign(this, {
        userId: id,
        fullName: fullname,
        userName: username,
        userRoles: roles,
        userGroups: groups,
      });

      this.hasRole("admin")
        ? router.push({ name: "users", params: { group: "admins" } })
        : router.push({
            name: "persons",
            params: { group: this.userGroups[0]["group"] },
          });
      storeClasses.classData.getClasses();
      storeAlert.alertMessage.setAlert();
    } catch (error) {
      storeAlert.alertMessage.setAlert("alert-warning", error as string);
      this.userLogout();
    }
  },

  userLogout: async function (): Promise<void> {
    try {
      const response = await storeAuth.axiosInstance.delete(`${server}/login`);
      console.log(response.status);
    } catch (error) {
      storeAlert.alertMessage.setAlert("alert-warning", error as string);
    }

    storeAuth.accessToken = "";
    storeAuth.refreshToken = "";

    router.push({ name: "login" });
  },

  hasRole: function (role: string): boolean {
    return this.userRoles.some((r: { role: any }) => r.role === role);
  },

  hasGroup: function (group: string): boolean {
    return this.userGroups.some((g: { group: any }) => g.group === group);
  },
});
</script>

<template>
  <NavBar 
    :fullName="userData.fullName" 
    :userLogout="userData.userLogout" 
  />
  <AlertMessage />
  <router-view />
  <FooterDiv />
</template>

<style>
html,
body {
  scrollbar-gutter: stable;
}
</style>
