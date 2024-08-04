<script setup lang="ts">
import { onBeforeMount } from "vue";
import { stateUser } from "../utils/state";

onBeforeMount(async () => {
  await stateUser.getCurrentUser();
});

async function userLogout(): Promise<void> {
  localStorage.removeItem("user_token");
  const router = useRouter();
  router.push("/login");
}
</script>

<template>
   <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>
