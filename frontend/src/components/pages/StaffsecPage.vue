<script setup lang="ts">
import axios from "axios";
import { defineAsyncComponent, onBeforeMount } from "vue";
import { stateClassify } from "@/state";
import { server } from "@/utilities";
import { router } from "@/router";

const NavBar = defineAsyncComponent(
  () => import("@components/content/layouts/NavBar.vue")
);
const MenuBar = defineAsyncComponent(
  () => import("@components/content/layouts/MenuBar.vue")
);

onBeforeMount(async () => {
  try {
    const response = await axios.get(`${server}/classes`);
    [
      stateClassify.regions,
      stateClassify.status,
      stateClassify.conclusions,
      stateClassify.relations
    ] = response.data;
  } catch (error) {
    console.error(error);
  }
  router.push({ name: "persons" });
});

</script>

<template>
  <div class="container-fluid row px-3">
    <div class="col-2">
      <NavBar/>
    </div>
    <div class="col-9">
      <MenuBar/>
      <router-view v-slot="{ Component }">
        <transition name="fade">
          <div><component :is="Component"/></div>
        </transition>
      </router-view>
    </div>
    <div class="col-1"></div>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
