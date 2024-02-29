<script setup lang="ts">
import { defineAsyncComponent } from "vue";
import { alertStore } from "@store/alert";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/layouts/HeaderDiv.vue")
);
const LoginForm = defineAsyncComponent(
  () => import("@components/content/login/forms/LoginForm.vue")
);
const AlertMessage = defineAsyncComponent(
  () => import("@components/content/login/layouts/AlertMessage.vue")
);
const FooterDiv = defineAsyncComponent(
  () => import("@components/content/login/layouts/FooterDiv.vue")
);

const storeAlert = alertStore();

storeAlert.alertMessage.setAlert(
  "alert-info", "Авторизуйтесь для входа в систему"
);
</script>

<template>
  <AlertMessage/>
  <div class="container">
    <div class="row justify-content-center">
      <div class="align-middle col col-6">
        <HeaderDiv :page-header="'StaffSec - кадровая безопасность'" />
        <LoginForm />
      </div>
    </div>
  </div>
  <FooterDiv />
</template>

<style scoped>
.container {
  height: 75vh;
  width: 75vh;
}
</style>
