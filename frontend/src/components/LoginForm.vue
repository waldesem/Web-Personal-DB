<script setup lang="ts">

import { ref, computed } from 'vue';
import axios from 'axios';
import config from '../config';
import router from '../router';
import AlertMessage from './AlertMessage.vue';

const login = ref({
  username: '',
  password: '',
  new_pswd: '',
  conf_pswd: ''
});

const data = ref({
  alert: '',
  path: 'login',
});

async function submitData(path: String) {
  if (path === 'password') {
    if (login.value.password === login.value.new_pswd) {
      data.value.alert = 'Match'
      return
    };
    if (login.value.conf_pswd !== login.value.new_pswd && path === 'password') { 
      data.value.alert = 'NoMatch';
      return
    }
  };
    try {
      const response = path === 'password'
        ? await axios.post(`${config.appUrl}/auth/password`, login.value, {
          headers: {'Authorization': `Bearer ${localStorage.getItem('access_token')}`}
        })
        : await axios.post(`${config.appUrl}/auth/login`, login.value);
      const { access, access_token, refresh_token } = response.data;
      data.value.alert = access;
      
      switch (access){
        case "Success":
          data.value.path = 'login';
          break;
        case "Authorized":
          localStorage.setItem('access_token', access_token);
          localStorage.setItem('refresh_token', refresh_token);
          router.push({ name: 'index', params: { flag: 'new', page: 1 } });
          break;
        case "Overdue":
          data.value.path = 'password';
          break;
      }
    } catch (error) {
      console.error(error)
    }
}

const attrAndText = computed(() => {
  const alerts = {
    Authorized: [],
    Denied: ['alert-danger', 'Неверный логин или пароль'],
    Overdue: ['alert-warning', 'Пароль просрочен. Измените пароль'],
    Success: ['alert-success', 'Пароль установлен. Войдите с новым паролем'],
    Default: ['alert-info', 'Авторизуйтесь для входа в систему'],
    NoMatch: ['alert-warning', 'Новый пароль и подтверждение не совпадают'],
    Match: ['alert-warning', 'Старый и новый пароли совпадают'],
  };
  return alerts[data.value.alert as keyof typeof alerts] as [string, string];
});

</script>

<template>
  <div class="container px-5 py-5 w-50">
    <div class="text-primary text-opacity-75 py-5">
      <h2>StaffSec - кадровая безопасность</h2>
    </div>
    <div class="border border-primary px-5 py-5">
      <AlertMessage v-if="attrAndText" :attr="attrAndText[0]" :text="attrAndText[1]" />
      <h5>{{data.path === 'login' ? 'Вход в систему' : 'Изменить пароль'}}</h5>
      <div class ="py-3">
        <form @submit.prevent="submitData(data.path)" class="form form-check" role="form">
          <div class="mb-3 row required">
              <label class="col-form-label col-lg-2" for="username">Логин: </label>
              <div class="col-lg-6">
                <input autocomplete="username" class="form-control" required id="username" name="username"  type="text"
                v-model.trim="login.username" minlength="5" maxlength="25" pattern="[a-zA-Z]+">
              </div>
          </div>
          <div class="mb-3 row required">
              <label class="col-form-label col-lg-2" for="password">Пароль: </label>
                  <div class="col-lg-6">
                    <input autocomplete="current-password" class="form-control" required id="password" name="password" type="password" 
                    v-model.trim="login.password" minlength="4" maxlength="25" pattern="[0-9a-zA-Z]+">
                    <div v-if="data.path ==='login'" class="py-2">
                      <a @click="data.path = 'password'" href="#">Изменить пароль</a>
                    </div>
                  </div>
              </div>
          <div v-if="data.path === 'password'">
            <div class="mb-3 row required">
              <label class="col-form-label col-lg-2" for="new_pswd">Новый: </label>
                <div class="col-lg-6">
                    <input autocomplete="current-password" class="form-control" required name="new_pswd" type="password" 
                    v-model.trim="login.new_pswd" minlength="5" maxlength="25" pattern="[0-9a-zA-Z]+">
                </div>
            </div>
            <div class="mb-3 row required">
              <label class="col-form-label col-lg-2" for="conf_pswd">Повтор: </label>
                <div class="col-lg-6">
                    <input autocomplete="current-password" class="form-control" required name="conf_pswd" type="password" 
                    v-model.trim="login.conf_pswd" minlength="5" maxlength="25" pattern="[0-9a-zA-Z]+">
                </div>
            </div>
          </div>
          <div class=" row">
              <div class="offset-lg-2 col-lg-">
                  <button class="btn btn-primary btn-md" name="submit" type="submit">{{data.path === 'login' ? 'Войти' : 'Изменить'}}</button>
              </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
../router/router