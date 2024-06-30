<script setup lang="ts">
import { axiosAuth, authErrorHandler } from "@/auth";
import { defineAsyncComponent, onBeforeMount } from "vue";
import { stateClassify, stateUser } from "@/state";
import { server } from "@/utilities";
import { router } from "@/router";

const NavBar = defineAsyncComponent(
  () => import("@components/content/elements/NavBar.vue")
);
const MenuBar = defineAsyncComponent(
  () => import("@components/content/elements/MenuBar.vue")
);

onBeforeMount(async () => {
  try {
    const response = await axiosAuth.get(`${server}/classes`);
    [
      stateClassify.regions,
      stateClassify.status,
      stateClassify.conclusions,
      stateClassify.relations,
      stateClassify.affilations,
      stateClassify.educations,
      stateClassify.addresses,
      stateClassify.contacts,
      stateClassify.documents,
      stateClassify.poligrafs,
    ] = response.data;

    const token = localStorage.getItem("user_token") as string;
    const payload = window.atob(token).split(":");
    stateUser.userId = payload[1];
    stateUser.username = payload[2];
    stateUser.hasAdmin = payload[3] == "1";

    router.push({ name: "persons" });
  } catch (error: any) {
    authErrorHandler(error);
  }
});
</script>

<template>
  <div class="container-fluid row px-3">
    <div class="col-2 d-print-none">
      <NavBar />
    </div>
    <div class="col-9" id="staffsec">
      <MenuBar />
      <router-view v-slot="{ Component }" :key="$route.fullPath">
        <div><component :is="Component" /></div>
      </router-view>
    </div>
    <div class="col-1 d-print-none"></div>
  </div>
</template>

<style scoped>
@media print {
  #staffsec {
    width: 100% !important;
  }
}
</style>
