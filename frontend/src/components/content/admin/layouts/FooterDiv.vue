<script setup lang="ts">
import { defineAsyncComponent, inject } from "vue";

const FooterDiv = defineAsyncComponent(
  () => import("@components/layouts/FooterDiv.vue")
);

const hasAdmin = inject("hasAdmin") as boolean;
</script>

<template>
  <FooterDiv>
    <template v-slot:footer>
      <router-link
        :hidden="hasAdmin"
        title="Candidates"
        :to="{name: 'persons' }"
      >
        Candidates
      </router-link>
    </template>
  </FooterDiv>
</template>
