<script setup lang="ts">

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
</script>

<template>
  <NuxtLoadingIndicator color="red" />
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>