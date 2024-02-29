<script setup lang="ts">
import { defineAsyncComponent } from "vue";

const FooterDiv = defineAsyncComponent(
  () => import("@components/layouts/FooterDiv.vue")
);
</script>

<template>
  <FooterDiv />
</template>
