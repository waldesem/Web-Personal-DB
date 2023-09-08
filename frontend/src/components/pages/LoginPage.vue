<script setup lang="ts">

import { appLogin } from '@store/login';
import { appAlert } from '@store/alert';
import AlertMessage from '@layouts/AlertMessage.vue';
import LoginForm from '@content/forms/LoginForm.vue';

const storeLogin = appLogin();
const storeAlert = appAlert();

storeAlert.alertAttr = 'alert-info';
storeAlert.alertText = 'Авторизуйтесь для входа в систему';

</script>

<template>
  <div class="container px-5 py-5 w-50">
    <div class="text-primary text-opacity-75 py-5">
      <h2>Деператамент экономической безопасности</h2>
    </div>
    <div class="border border-primary px-5 py-5">
      <AlertMessage />
      <h5>{{ storeLogin.action === 'login' ? 'Вход в систему' : 'Изменить пароль' }}</h5>
      <LoginForm />
    </div>
  </div>
</template>
