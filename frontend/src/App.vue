<script setup lang="ts">
import axios from "axios";
import { computed, watch, onBeforeMount, onMounted } from "vue";
import { stateClassify, stateUser, stateAlert } from "@/state";
import { router } from "@/router";
import { readToken, server } from "@/utilities";

watch(
  () => localStorage.getItem("refresh_token"),
  (newToken) => {
    const tokenPayload = readToken(newToken as string);
    stateUser.userId = tokenPayload["id"] ? tokenPayload["id"] : "";
    stateUser.fullName = tokenPayload["fullname"] ? tokenPayload["fullname"] : "";
    stateUser.userName = tokenPayload["username"] ? tokenPayload["username"] : "";
    stateUser.userRoles = tokenPayload["roles"] ? tokenPayload["roles"] : [];
  },
  { immediate: true }
);

computed(() => {
  stateUser.hasAdmin = stateUser.userRoles.some((r: { role: any }) => r.role === "admin")
});

onBeforeMount(async () => {
  await getClasses();
  stateAlert.setAlert();
});

onMounted(() => {
  router.push({ name: "persons" });
});

async function getClasses(): Promise<void> {
  try {
    const response = await axios.get(`${server}/classes`);
    [
      stateClassify.conclusions,
      stateClassify.roles,
      stateClassify.status,
      stateClassify.regions,
      stateClassify.users,
    ] = response.data;
  } catch (error) {
    console.error(error);
  }
}
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
