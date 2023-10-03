<script setup lang="ts">

import { loginStore } from '@store/login';
import { alertStore } from '@store/alert';
import LoginForm from '@content/forms/LoginForm.vue';

const storeLogin = loginStore();
const storeAlert = alertStore();

storeAlert.setAlert('alert-info', 'Авторизуйтесь для входа в систему');

</script>

<template>
  <div class="container px-5 py-3 w-50">
    <div class="text-primary text-opacity-75 py-3">
      <h2>EconSec - экономическая безопасность</h2>
    </div>
    <div class="border border-primary px-5 py-5">
      <h5>{{ storeLogin.action === 'login' ? 'Вход в систему' : 'Изменить пароль' }}</h5>
      <LoginForm />
    </div>
  </div>
</template>
