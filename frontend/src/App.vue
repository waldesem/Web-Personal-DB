<script setup lang="ts">
import axios from "axios";
import { onMounted } from "vue";
import { stateClassify } from "@/state";
import { server } from "@/utilities";
import { router } from "@/router";

onMounted(async () => {
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

  try {
    const response = await axios.get(`${server}/users/admin`);
    if (response.status === 204) {
      router.push({ name: "persons" })
    } else {
      router.push({ name: "admin" })
    }
  } catch (error) {
    console.error(error);
  }
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
