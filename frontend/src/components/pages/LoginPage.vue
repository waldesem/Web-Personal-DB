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
</script>

<template>
  <div class="container pt-5">
    <AlertMessage/>
    <HeaderDiv 
      :cls="'text-danger py-3'"
      :page-header="'StaffSec - кадровая безопасность'"/>
    <LoginForm/>
  </div>
</template>

<style scoped>
.container {
  justify-content: center;
  align-items: center;
  width: fit-content;
}
</style>
