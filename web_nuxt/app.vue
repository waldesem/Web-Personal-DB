<script setup lang="ts">
// import { stateClassify, stateUser, userToken } from "@/state/state";

useHead({
  title: "StaffSec - кадровая безопасность",
  meta: [
    { name: 'description', content: 'Кадровая безопасность' }
  ],
})

useSeoMeta({
  title: 'StaffSec - кадровая безопасность',
  ogTitle: 'StaffSec - кадровая безопасность',
  description: 'Кадровая безопасность, проверка персонала',
  ogDescription: 'Кадровая безопасность, проверка персонала',
})

// const classifyState = stateClassify();

// const { data } = await useAsyncData("classify", async () => {
//   const response = await $fetch(`${server}/classes`);
//   return response;
// });
// classifyState.classes.value = data.value;

// const userState = stateUser();

// userState.user.value = computed(() => {
//   if (!userToken.value) {
//     return navigateTo("/login");
//   }
//   return JSON.parse(
//       Buffer.from(userToken.value.split(".")[1], "base64").toString()
//     ) as User
// });
</script>

<template>
  <NuxtLoadingIndicator color="red" />
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
  <UNotifications />  
</template>

<style>
.slide-fade-enter-active {
  transition: all 0.1s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.1s ease-in;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(20px);
  opacity: 0;
}
</style>