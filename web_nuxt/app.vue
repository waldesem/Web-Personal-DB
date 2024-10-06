<script setup lang="ts">
useHead({
  title: "StaffSec - кадровая безопасность",
  meta: [{ name: "description", content: "Кадровая безопасность" }],
});

useSeoMeta({
  title: "StaffSec - кадровая безопасность",
  ogTitle: "StaffSec - кадровая безопасность",
  description: "Кадровая безопасность, проверка персонала",
  ogDescription: "Кадровая безопасность, проверка персонала",
});
</script>

<template>
  <NuxtLoadingIndicator color="red" />
  <NuxtLayout>
    <NuxtPage :keepalive="{ include: 'persons' }" :max="5" />
  </NuxtLayout>
  <UNotifications />
</template>

<style>
.page-enter-active,
.page-leave-active,
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.2s;
}
.page-enter-from,
.page-leave-to {
  opacity: 0;
}
.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(10px);
  opacity: 0;
}
</style>
