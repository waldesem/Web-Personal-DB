<script setup lang="ts">

import axios from 'axios';
import { ref } from 'vue';
import { onBeforeRouteLeave } from 'vue-router';
import { loginStore } from '@store/login';
import { alertStore } from '@store/alert';
import { server, clearItem } from '@share/utilities';

const storeLogin = loginStore();
const storeAlert = alertStore();

const formData: Record<string, any> = ref({}); 
const formAction = ref('login');
const hidePassword = ref(true);

onBeforeRouteLeave((_to: any, _from: any, next: () => void) => {
  clearItem(formData.value)
  next()
});

/**
 * Submits data to the server.
 *
 * @return {Promise<void>} - A promise that resolves when the data is submitted.
 */
 async function submitLogin(): Promise<void> {

  if (formAction.value === 'password') {
    if (formData['password'] === formData['new_pswd']) {
      storeAlert.setAlert('alert-warning', 'Старый и новый пароли совпадают');
      return
    };
    if (formData['conf_pswd'] !== formData['new_pswd']) {
      storeAlert.setAlert('alert-warning', 'Новый пароль и подтверждение не совпадают');
      return
    }
  };
  try {
    const response = formAction.value === 'password'
      ? await axios.patch(`${server}/login`, formData)
      : await axios.post(`${server}/login`, formData);
    
    const { message, access_token, refresh_token } = response.data;
    
    hidePassword.value = true;
    clearItem(formData.value)

    switch (message) {
      case 'Authenticated':

        if (formAction.value === 'password') {
          formAction.value = 'login';
          storeAlert.alertMessage.attrAlert = 'alert-success';
          storeAlert.alertMessage.textAlert = 'Войдите с новым паролем';
        } else {          
          localStorage.setItem('refresh_token', refresh_token);
          localStorage.setItem('access_token', access_token);
          storeLogin.getAuth();
        };
        break;

      case 'Overdue':
        formAction.value = 'password';
        storeAlert.setAlert('alert-warning', 'Пароль просрочен. Измените пароль');
        break;

      case 'Denied':
        formAction.value = 'login';
        storeAlert.setAlert('alert-danger', 'Неверный логин или пароль');
        break;
    };
  } catch (error) {
    storeAlert.setAlert('alert-warning', error as string);
    storeLogin.userLogout();
  };
};

</script>

<template>
  <h5>{{ formAction === 'login' ? 'Вход в систему' : 'Изменить пароль' }}</h5>
  <div class="py-3">
    <form @submit.prevent="submitLogin" class="form form-check" role="form">
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="username">Логин: </label>
        <div class="col-lg-6">
          <input autocomplete="username" class="form-control" required 
            id="username" name="username" type="text" minlength="4" maxlength="16" 
            placeholder="Логин пользователя" pattern="[a-zA-Z]+"
            v-model.trim="formData['username']">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="password">Пароль: </label>
        <div class="col-lg-6">
          <div class="input-group">
            <input autocomplete="current-password" class="form-control" required 
                  id="password" name="password" minlength="8" maxlength="16" 
                  placeholder="Пароль пользователя" pattern="[0-9a-zA-Z]+"
                  :type="hidePassword ? 'password' : 'text'" 
                  v-model.trim="formData['password']" >
            <span class="input-group-text">
              <a role="button" @click="hidePassword = !hidePassword">
                <i :class="hidePassword ? 'bi bi-eye' : 'bi bi-eye-slash'"></i>
              </a>
            </span>
          </div>
          <div v-show="formAction === 'login'" class="py-2">
            <a @click="formAction = 'password'" href="#">Изменить пароль</a>
          </div>
        </div>
      </div>
      <div v-if="formAction === 'password'">
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="new_pswd">Новый: </label>
          <div class="col-lg-6">
            <input autocomplete="current-password" class="form-control" required 
                  name="new_pswd" minlength="8" maxlength="16"
                  placeholder="От 8 до 16 символов: a-z, A-Z" pattern="[0-9a-zA-Z]+"
                  :type="hidePassword ? 'password' : 'text'"
                  v-model.trim="formData['new_pswd']">
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="conf_pswd">Повтор: </label>
          <div class="col-lg-6">
            <input autocomplete="current-password" class="form-control" required 
                  name="conf_pswd" minlength="8" maxlength="16" 
                  placeholder="Повторите новый пароль" pattern="[0-9a-zA-Z]+"
                  :type="hidePassword ? 'password' : 'text'"
                  v-model.trim="formData['conf_pswd']">
          </div>
        </div>
      </div>
      <div class="row mb-3">
        <div class="offset-lg-2 col-lg-10">
            <button class="btn btn-primary btn-md" name="submit" type="submit">
              {{ formAction === 'login' ? 'Войти' : 'Изменить' }}
            </button>              
              &nbsp;
            <button v-show="formAction === 'password'" class="btn btn-secondary btn-md" 
                    type="button" @click="formAction = 'login'">Отменить
            </button>
        </div>
      </div>
    </form>
  </div>
</template>