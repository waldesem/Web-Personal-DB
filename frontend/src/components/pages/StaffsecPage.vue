<script setup lang="ts">
import { defineAsyncComponent } from "vue";
import { onMounted } from "vue";
import { axiosAuth } from "@/auth";
import { server } from "@/utilities";
import { stateUser, stateAlert, stateMessage } from "@/state";

const NavBar = defineAsyncComponent(
  () => import("@components/content/layouts/NavBar.vue")
);
const MenuBar = defineAsyncComponent(
  () => import("@components/content/layouts/MenuBar.vue")
);

onMounted(async () => {
  try {
    const response = await axiosAuth.get(`${server}/auth`);
    const { id, fullname, username, roles } = response.data;
    stateUser.userId = id;
    stateUser.fullName = fullname;
    stateUser.userName = username;
    stateUser.hasAdmin = roles.includes("admin");
    await stateMessage.updateMessages();
  } catch (error) {
    stateAlert.setAlert("alert-warning", error as string);
  }
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
