<script setup lang="ts">
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap-icons/font/bootstrap-icons.min.css";

// eslint-disable-next-line no-undef
useHead({
  title: "StaffSec - кадровая безопасность",
  meta: [
    { name: 'description', content: 'Кадровая безопасность' }
  ],
  bodyAttrs: {
    class: 'test'
  },
  script: [ { innerHTML: 'console.log(\'Hello world\')' } ]
})

// eslint-disable-next-line no-undef
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