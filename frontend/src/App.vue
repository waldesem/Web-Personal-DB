<script setup lang="ts">
import axios from "axios";
import { computed, watch, onBeforeMount, onMounted } from "vue";
import { stateClassify, stateUser, stateToken } from "@/state";
import { readToken, server } from "@/utilities";
import { router } from "@/router";

watch(
  () => stateToken.accessToken,
  (newToken) => {
    const tokenPayload = readToken(newToken as string);
    stateUser.userId = tokenPayload["id"];
    stateUser.fullName = tokenPayload["fullname"];
    stateUser.userName = tokenPayload["username"];
    stateUser.userRoles = tokenPayload["roles"];
  },
  { immediate: true }
);

computed(() => {
  stateUser.hasAdmin = stateUser.userRoles.some(
    (r: { role: any }) => r.role === "admin"
  );
});

onBeforeMount(async () => {
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
});

onMounted(() => {
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
