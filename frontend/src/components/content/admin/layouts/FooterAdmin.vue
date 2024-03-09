<script setup lang="ts">
import { defineAsyncComponent } from "vue";

const FooterDiv = defineAsyncComponent(
  () => import("@components/layouts/FooterDiv.vue")
);

</script>

<template>
  <FooterDiv>
    <template v-slot:footer>
      <router-link
        title="Candidates"
        :to="{ name: 'persons' }"
      >
        Candidates
      </router-link>
    </template>
  </FooterDiv>
</template>
