<script setup lang="ts">

import { alertStore } from '@store/alert';

const LoginForm = () => import('@components/forms/LoginForm.vue');
const HeaderDiv = () => import('@components/layouts/HeaderDiv.vue');

const storeAlert = alertStore();

storeAlert.alertMessage.attrAlert = 'alert-info';
storeAlert.alertMessage.textAlert = 'Авторизуйтесь для входа в систему';

</script>

<template>
  <div class="container py-3">
    <div class="row py-5">
      <div class="col col-3"></div>
      <div class="col col-6">
        <HeaderDiv :page-header="'StaffSec - кадровая безопасность'" />
        <LoginForm />
      </div>
      <div class="col col-3"></div>
    </div>
  </div>
</template>