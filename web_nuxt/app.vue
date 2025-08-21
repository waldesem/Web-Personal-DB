<script setup lang="ts">
useHead({
  htmlAttrs: { lang: "ru" },
  link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
  meta: [
    { name: "description", content: "Кадровая безопасность" },
    { name: "viewport", content: "width=device-width, initial-scale=1" },
    { charset: "utf-8" },
  ],
  
});
</script>

<template>
  <UApp>
    <NuxtLoadingIndicator color="red" :height="5" />
    <NuxtLayout>
      <NuxtPage
        :transition="{
          name: 'page',
        }"
      />
    </NuxtLayout>
  </UApp>
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
/* 
html,
body {
  scrollbar-gutter: stable;
} */
</style>
