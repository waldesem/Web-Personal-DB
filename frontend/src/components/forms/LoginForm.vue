<script setup lang="ts">

import axios from 'axios';
import { onBeforeRouteLeave } from 'vue-router';
import { loginStore } from '@store/login';
import { alertStore } from '@store/alert';
import { authStore } from '@store/token'
import { server } from '@share/utilities';

const storeLogin = loginStore();
const storeAlert = alertStore();
const storeAuth = authStore();

let loginData = {
  username: '',
  password: '',
  new_pswd: '',
  conf_pswd: ''
};

let action = 'login';

let hidePassword = true;

onBeforeRouteLeave((_to: any, _from: any, next: () => void) => {
  Object.assign(loginData, {
    username: '',
    password: '',
    new_pswd: '',
    conf_pswd: ''
  });
  next()
});

/**
 * Submits data to the server.
 *
 * @return {Promise<void>} - A promise that resolves when the data is submitted.
 */
 async function submitLogin(): Promise<void> {

if (action === 'password') {
  if (loginData.password === loginData.new_pswd) {
  storeAlert.setAlert('alert-warning', 
                      'Старый и новый пароли совпадают');
  return
  };
  if (loginData.conf_pswd !== loginData.new_pswd) {
    storeAlert.setAlert('alert-warning', 
                        'Новый пароль и подтверждение не совпадают');
    return
  }
};
try {
  const response = action === 'password'
    ? await axios.patch(`${server}/login`, loginData)
    : await axios.post(`${server}/login`, loginData);
  
  const { message, access_token, refresh_token } = response.data;

  switch (message) {
    case 'Authenticated':

      if (action === 'password') {
        action = 'login';
        storeAlert.setAlert('alert-success',
                            'Пароль установлен. Войдите с новым паролем');
      } else {
        localStorage.setItem('access_token', access_token);
        localStorage.setItem('refresh_token', refresh_token);
        
        storeAuth.setRefreshToken(refresh_token);
        storeAuth.setAccessToken(access_token);
        
        document.getElementById('openModal')?.click();
        setTimeout(() => document.getElementById('closeModal')?.click(), 3000)
        storeLogin.getAuth();
      };
      break;

    case 'Overdue':
      action = 'password';
      storeAlert.setAlert('alert-warning', 
                          'Пароль просрочен. Измените пароль');
      break;

    case 'Denied':
      action = 'login';
      storeAlert.setAlert('alert-danger', 
                          'Неверный логин или пароль');
      break;
  }
} catch (error) {
  console.error(error)
  storeAlert.setAlert('alert-danger', 
                      'Ошибка авторизации');
  action = 'login';
  storeLogin.userLogout();
};
};

</script>

<template>
  <h5>{{ action === 'login' ? 'Вход в систему' : 'Изменить пароль' }}</h5>
  <div class="py-3">
    <form @submit.prevent="submitLogin" class="form form-check" role="form">
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="username">Логин: </label>
        <div class="col-lg-6">
          <input autocomplete="username" class="form-control" required 
            id="username" name="username" type="text" minlength="4" maxlength="16" 
            placeholder="Логин пользователя" pattern="[a-zA-Z]+"
            v-model.trim="loginData.username">
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
                  v-model.trim="loginData.password" >
            <span class="input-group-text">
              <a role="button" @click="hidePassword = !hidePassword">
                <i :class="hidePassword ? 'bi bi-eye' : 'bi bi-eye-slash'"></i>
              </a>
            </span>
          </div>
          <div v-show="action === 'login'" class="py-2">
            <a @click="action = 'password'" href="#">Изменить пароль</a>
          </div>
        </div>
      </div>
      <div v-show="action === 'password'">
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="new_pswd">Новый: </label>
          <div class="col-lg-6">
            <input autocomplete="current-password" class="form-control" required 
                  name="new_pswd" minlength="8" maxlength="16"
                  placeholder="От 8 до 16 символов: a-z, A-Z" pattern="[0-9a-zA-Z]+"
                  :type="hidePassword ? 'password' : 'text'"
                  v-model.trim="loginData.new_pswd">
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="conf_pswd">Повтор: </label>
          <div class="col-lg-6">
            <input autocomplete="current-password" class="form-control" required 
                  name="conf_pswd" minlength="8" maxlength="16" 
                  placeholder="Повторите новый пароль" pattern="[0-9a-zA-Z]+"
                  :type="hidePassword ? 'password' : 'text'"
                  v-model.trim="loginData.conf_pswd">
          </div>
        </div>
      </div>
      <div class="row">
        <div class="offset-lg-2 col-lg-10">
          <div class="btn-group" role="group">
            <button class="btn btn-primary btn-md" name="submit" type="submit">
              {{ action === 'login' ? 'Войти' : 'Изменить' }}
            </button>
            <button v-show="action === 'password'" class="btn btn-primary btn-md" 
                    type="button" @click="action = 'login'">Отменить
            </button>
          </div>
        </div>
      </div>
    </form>
  </div>
</template>