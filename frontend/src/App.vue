<script setup lang="ts">
import axios from "axios";
import { watch, onBeforeMount, onMounted } from "vue";
import { stateClassify, stateUser, stateToken, stateAlert } from "@/state";
import { axiosAuth } from "@/auth";
import { server } from "@/utilities";
import { router } from "@/router";

watch(
  () => stateToken.accessToken,
  async () => {
    try {
      const response = await axiosAuth.get(`${server}/login`);
      const { id, fullname, username, roles } = response.data;
      stateUser.userId = id;
      stateUser.fullName = fullname;
      stateUser.userName = username;
      stateUser.hasAdmin = roles.some(
        (r: { role: any }) => r.role === "admin"
      );
    } catch (error) {
      stateAlert.setAlert("alert-warning", error as string);
    }
  },
);

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
