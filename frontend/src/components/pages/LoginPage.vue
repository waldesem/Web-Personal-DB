<script setup lang="ts">
import { defineAsyncComponent } from "vue";
import { alertStore } from "@store/alert";

const LoginForm = defineAsyncComponent(
  () => import("@components/forms/LoginForm.vue")
);
const HeaderDiv = defineAsyncComponent(
  () => import("@components/layouts/HeaderDiv.vue")
);

const storeAlert = alertStore();

storeAlert.alertMessage.setAlert(
  "alert-info", "Авторизуйтесь для входа в систему"
);
</script>

<template>
  <div class="container">
    <div class="row justify-content-center">
      <div class="align-middle col col-6">
        <HeaderDiv :page-header="'StaffSec - кадровая безопасность'" />
        <LoginForm />
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  height: 75vh;
  width: 75vh;
}
</style>
