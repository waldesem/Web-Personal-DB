<script setup lang="ts">
import { defineAsyncComponent } from "vue";
import { userStore } from "@/store/user";

const FooterDiv = defineAsyncComponent(
  () => import("@components/layouts/FooterDiv.vue")
);

const storeUser = userStore();
</script>

<template>
  <FooterDiv>
    <template v-slot:footer>
      <router-link v-if="storeUser.userData.hasAdmin"
        title="Admin"
        :to="{name: 'users' }"
      >
        Admin
      </router-link>
    </template>
  </FooterDiv>
</template>
