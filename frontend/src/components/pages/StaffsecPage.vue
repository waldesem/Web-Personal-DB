<script setup lang="ts">
import axios from "axios";
import { defineAsyncComponent, onBeforeMount, onMounted } from "vue";
import { stateClassify, stateUser } from "@/state";
import { server } from "@/utilities";
import { router } from "@/router";

const NavBar = defineAsyncComponent(
  () => import("@components/content/layouts/NavBar.vue")
);
const MenuBar = defineAsyncComponent(
  () => import("@components/content/layouts/MenuBar.vue")
);

onBeforeMount( () => {
  const token = localStorage.getItem("user_token") as string;
  if (!token) {
    router.push({ name: "login" });
  }
  const payload = decodeURIComponent(escape(window.atob(token))).split(":");
  stateUser.userId = payload[1];
  stateUser.username = payload[2];
  stateUser.hasAdmin = payload[3] === "1";
});

onMounted(async () => {
  try {
    const response = await axios.get(`${server}/classes`);
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
      stateClassify.poligrafs
    ] = response.data;
  } catch (error) {
    console.error(error);
  }
  router.push({ name: "persons" });
});

</script>

<template>
  <div class="container-fluid row px-3">
    <div class="col-2 d-print-none ">
      <NavBar/>
    </div>
    <div class="col-9" id="staffsec">
      <MenuBar/>
      <router-view v-slot="{ Component }" :key="$route.fullPath">
        <div><component :is="Component"/></div>
      </router-view>
    </div>
    <div class="col-1 d-print-none "></div>
  </div>
</template>

<style scoped>
@media print{
  #staffsec {
    width: 100% !important;
  }
}
</style>
