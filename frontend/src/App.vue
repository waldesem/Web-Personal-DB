<script setup lang="ts">
import { onMounted } from "vue";
import { stateUser } from "@/state";
import { router } from "@/router";

onMounted( () => {
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
  router.push({ name: "persons" });
});
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
