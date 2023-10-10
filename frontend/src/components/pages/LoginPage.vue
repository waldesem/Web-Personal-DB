<script setup lang="ts">

import { onBeforeRouteLeave } from 'vue-router';
import { loginStore } from '@store/login';
import { alertStore } from '@store/alert';
import LoginForm from '@components/forms/LoginForm.vue'

const storeLogin = loginStore();
const storeAlert = alertStore();

storeAlert.alertMessage.attrAlert = 'alert-info';
storeAlert.alertMessage.textAlert = 'Авторизуйтесь для входа в систему';

onBeforeRouteLeave((_to: any, _from: any, next: () => void) => {
  Object.assign(storeLogin.loginData, {
    username: '',
    password: '',
    new_pswd: '',
    conf_pswd: ''
  });
  next()
});

</script>

<template>
  <div class="container py-5">
    <div class="row">
      <div class="col col-3"></div>
      <div class="col col-6">
        <div class="text-primary text-opacity-75 py-3">
          <h2>StaffSec - кадровая безопасность</h2>
        </div>
        <LoginForm />
      </div>
      <div class="col col-3"></div>
    </div>
  </div>
</template>
