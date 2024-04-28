<script setup lang="ts">
import { defineAsyncComponent } from "vue";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/content/elements/HeaderDiv.vue")
);
const AlertMessage = defineAsyncComponent(
  () => import("@components/content/elements/AlertMessage.vue")
);
const LoginForm = defineAsyncComponent(
  () => import("@components/content/forms/LoginForm.vue")
);
const FooterDiv = defineAsyncComponent(
  () => import("@components/content/layouts/FooterDiv.vue")
);
</script>

<template>
  <div class="container">
    <AlertMessage/>
    <HeaderDiv 
      :cls="'text-info py-3'"
      :page-header="'StaffSec - кадровая безопасность'"/>
    <LoginForm/>
  </div>
  <FooterDiv/>
</template>

<style scoped>
.container {
  height: 65vh;
  width: 50vh;
  margin-top: 10vh;
}
</style>
