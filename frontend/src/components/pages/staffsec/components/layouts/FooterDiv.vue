<script setup lang="ts">
import { defineAsyncComponent } from "vue";

const FooterDiv = defineAsyncComponent(
  () => import("@components/layouts/FooterDiv.vue")
);

const prop = defineProps(['hasAdmin'])
</script>

<template>
  <FooterDiv>
    <template v-slot:footer>
      <router-link
        :hidden="prop.hasAdmin"
        title="Admin"
        :to="{name: 'users' }"
      >
        Admin
      </router-link>
    </template>
  </FooterDiv>
</template>
