<script setup lang="ts">
import { defineAsyncComponent, watch } from "vue";
import { onMounted } from "vue";
import { stateMessage, stateUser } from "@/state";

const NavBar = defineAsyncComponent(
  () => import("@components/content/layouts/NavBar.vue")
);
const MenuBar = defineAsyncComponent(
  () => import("@components/content/layouts/MenuBar.vue")
);

onMounted(async () => {
  await stateMessage.updateMessages();
});

watch(stateUser.userToken, (token: string) => {
  const payload = window.atob(token).split(":")
  stateUser.userId = payload[1];
  stateUser.hasAdmin = payload[2].includes("admin");
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
