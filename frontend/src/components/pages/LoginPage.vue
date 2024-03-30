<script setup lang="ts">
import { defineAsyncComponent } from "vue";
import { alertStore } from "@store/alert";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/content/elements/HeaderDiv.vue")
);
const AlertMessage = defineAsyncComponent(
  () => import("@components/content/layouts/AlertMessage.vue")
);
const LoginForm = defineAsyncComponent(
  () => import("@components/content/forms/LoginForm.vue")
);

const storeAlert = alertStore();

storeAlert.alertMessage.setAlert(
  "alert-info", "Авторизуйтесь для входа в систему"
);
</script>

<template>
  <AlertMessage/>
  <div class="container" id="login-page">
    <div class="row justify-content-center">
      <HeaderDiv :page-header="'StaffSec - кадровая безопасность'" />
      <LoginForm />
    </div>
  </div>
</template>

<style scoped>
#login-page {
  height: 75vh;
  width: 50vh;
}
</style>
