<script setup lang="ts">
useHead({
  title: "StaffSec - кадровая безопасность",
  meta: [{ name: "description", content: "Кадровая безопасность" }],
});
</script>

<template>
  <UApp>
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </UApp>
</template>

<style>
html,
body {
  scrollbar-gutter: stable;
}

.page-enter-active,
.page-leave-active,
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.1s;
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
