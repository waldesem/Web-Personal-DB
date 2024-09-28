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
    <NuxtPage />
  </NuxtLayout>
  <UNotifications />
</template>

<style>
.page-enter-active,
.page-leave-active {
  transition: all 0.2s;
}
.page-enter-from,
.page-leave-to {
  opacity: 0;
}

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
