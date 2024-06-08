<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount } from "vue";
import { stateUser } from "@/state";
import { router } from "@/router";

const NavBar = defineAsyncComponent(
  () => import("@components/content/layouts/NavBar.vue")
);
const MenuBar = defineAsyncComponent(
  () => import("@components/content/layouts/MenuBar.vue")
);

onBeforeMount(() => {
  const token = localStorage.getItem("user_token") as string;
  if (!token) {
    router.push({ name: "login" });
  }
  const payload = window.atob(token).split(":")
  stateUser.userId = payload[1];
  stateUser.fullname = payload[2];
  stateUser.username = payload[3];
  stateUser.region = payload[4];
  stateUser.hasAdmin = payload[5] === "1";
})
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
