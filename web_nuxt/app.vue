<script setup lang="ts">
import { useDocumentVisibility } from "@vueuse/core";
import type { Token } from "./types";

useHead({
  htmlAttrs: { lang: "ru" },
  link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
  meta: [
    { name: "description", content: "Кадровая безопасность" },
    { name: "viewport", content: "width=device-width, initial-scale=1" },
    { charset: "utf-8" },
  ],
});

const visibility = useDocumentVisibility();
watchEffect(async () => {
  if (visibility.value === "visible") {
    const { $api } = useNuxtApp();
    try {
      userState.value = (await $api("/routes/auth/session")) as Token;
    } catch (error) {
      console.error(error);
      await navigateTo("/login");
    }
  }
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
