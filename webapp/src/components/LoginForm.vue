<template>
  <div class="container px-5 py-5">
    <div class="border border-primary px-5 py-5">
      <AlertMessage :attr="data.attr" :text="data.text" />
      <h5>{{data.path === 'login' ? 'Вход в систему' : 'Изменить пароль'}}</h5>
      <div class ="py-3">
        <form @submit.prevent="submitData" class="form form-check" role="form">
          <div class="mb-3 row required">
              <label class="col-form-label col-lg-1" for="username">Логин: </label>
              <div class="col-lg-4">
                <input autocomplete="username" class="form-control" required id="username" name="username"  type="text"
                ref="login.username" minlength="5" maxlength="25" placeholder="Латинские буквы 8-25 символов" pattern="[a-zA-Z]+">
              </div>
          </div>
          <div class="mb-3 row required">
              <label class="col-form-label col-lg-1" for="password">Пароль: </label>
                  <div class="col-lg-4">
                    <input autocomplete="current-password" class="form-control" required id="password" name="password" type="password" 
                    ref="login.password" minlength="4" maxlength="25" placeholder="Латинские буквы и цифры 8-25 символов" pattern="[0-9a-zA-Z]+">
                    <div v-if="data.path ==='/login'" class="py-2">
                      <a @click="data.flag = 'Change'; data.path = 'password'" href="#">Изменить пароль</a>
                    </div>
                  </div>
              </div>
          <div v-if="data.path === '/password'">
            <div class="mb-3 row required">
              <label class="col-form-label col-lg-1" for="new_pswd">Новый: </label>
                <div class="col-lg-4">
                    <input autocomplete="current-password" class="form-control" required name="new_pswd" type="password" 
                    ref="login.new_pswd" minlength="5" maxlength="25" placeholder="Латинские буквы и цифры 8-25 символов" pattern="[0-9a-zA-Z]+">
                </div>
            </div>
            <div class="mb-3 row required">
              <label class="col-form-label col-lg-1" for="conf_pswd">Повтор: </label>
                <div class="col-lg-4">
                    <input autocomplete="current-password" class="form-control" required name="conf_pswd" type="password" 
                    ref="login.conf_pswd" minlength="5" maxlength="25" placeholder="Латинские буквы и цифры 8-25 символов" pattern="[0-9a-zA-Z]+">
                </div>
            </div>
          </div>
          <div class=" row">
              <div class="offset-lg-1 col-lg-4">
                  <button class="btn btn-primary btn-md" name="submit" type="submit">{{data.path === 'login' ? 'Войти' : 'Изменить'}}</button>
              </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">

import { ref, onBeforeMount, computed } from 'vue';
import axios from 'axios';
import config from '@/config';
import router from '@/router';
import AlertMessage from './AlertMessage.vue';

const login = ref({});
// username: ''
// password: ''
// new_pswd: ''
// conf_pswd: ''

const data = ref({
  flag: '',
  path: ''
});

async function submitData(event: Event) {
  console.log(login.value)
  if (data.value.new_pswd === data.value.new_pswd) {
    data.value.flag = 'Match'
  } else if (data.value.password === data.value.new_pswd) { 
    data.value.flag = 'NoMatch';
  } else {
    try {
      const response = await axios.post(`${config.appUrl}/${data.value.path}`, login.value);     
      const { access, access_token } = response.data;
      data.value.alert = access;
      switch (access){
        case "Success":
          data.value.flag = 'Logout';
          data.value.path = 'login';
          break;
        case "Authorized":
          localStorage.setItem('jwt_token', access_token);
          router.push({ name: 'index', params: { flag: 'new' } });
          break;
        case "Overdue":
          data.value.flag = 'Change';
          data.value.path = 'password';
          break;
      }
    } catch (error) {
      console.error(error)
    }
  }
}

const { attr, text } = computed(() => {
  const alerts = {
    Authorized: ['', ''],
    Change: ['alert-info', 'Заполните обязательные поля'],
    None: ['alert-danger', 'Неверный логин или пароль'],
    Overdue: ['alert-warning', 'Пароль просрочен. Измените пароль'],
    Denied: ['alert-danger', 'Пользователь не авторизован'],
    Success: ['alert-success', 'Пароль установлен. Войдите с новым паролем'],
    Default: ['alert-info', 'Авторизуйтесь для входа в систему'],
    NoMatch: ['alert-warning', 'Новый пароль и подтверждение не совпадают'],
    Match: ['alert-warning', 'Старый и новый пароли совпадают'],
  };
  return alerts[data.value.flag as keyof typeof alerts]
});

onBeforeMount(async () => {
  localStorage.removeItem('jwt_token');
  const response = await axios.get(`${config.appUrl}/logout`)
  console.log(response)
  data.value.flag = 'Logout';
  data.value.path = 'login';
});

</script>
