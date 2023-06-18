<template>
  <router-view></router-view>
  <div class="container px-5 py-5">
    <div class="border border-primary px-5 py-5">
      <AlertMessage :attr="attr" :text="text" />
      <h5>{{title}}</h5>
      <div class ="py-3">
        <form 
            @submit.prevent="submitData" class="form form-check" role="form">
          <div class="mb-3 row required">
              <label class="col-form-label col-lg-1" for="username">Логин: </label>
              <div class="col-lg-4">
                <input autocomplete="username" class="form-control" minlength="3" maxlength="25" name="username" placeholder="Латинские буквы 8-25 символов" required type="text" value="" pattern="[a-zA-Z]+">
              </div>
          </div>
          <div class="mb-3 row required">
              <label class="col-form-label col-lg-1" for="password">Пароль: </label>
                  <div class="col-lg-4">
                    <input autocomplete="current-password" class="form-control" minlength="3" maxlength="25" name="password" placeholder="Латинские буквы и цифры 8-25 символов" required type="password" value="" pattern="[0-9a-zA-Z]+">
                    <div v-if="path ==='/login'" class="py-2"><a @click="changePswd" href="#">Изменить пароль</a></div>
                  </div>
              </div>
          <div v-if="path === '/password'">
            <div class="mb-3 row required">
              <label class="col-form-label col-lg-1" for="new_pswd">Новый: </label>
                <div class="col-lg-4">
                    <input autocomplete="current-password" class="form-control" minlength="3" maxlength="25" 
                    name="new_pswd" placeholder="Новый пароль" required type="password" value="" pattern="[0-9a-zA-Z]+">
                </div>
            </div>
            <div class="mb-3 row required">
              <label class="col-form-label col-lg-1" for="conf_pswd">Повтор: </label>
                <div class="col-lg-4">
                    <input autocomplete="current-password" class="form-control" minlength="3" maxlength="25" 
                    name="conf_pswd" placeholder="Подтверждение пароля" required type="password" value="" pattern="[0-9a-zA-Z]+">
                </div>
            </div>
          </div>
          <div class=" row">
              <div class="offset-lg-1 col-lg-4">
                  <button class="btn btn-primary btn-md" name="submit" type="submit">{{ value }}</button>
              </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">

import { ref } from 'vue';
import axios from 'axios';
import router from '../router';
import AlertMessage from './AlertMessage.vue';

const attr = ref('alert-info');
const text = ref('Авторизуйтесь для входа в систему');
const title = ref('Вход в систему');
const path = ref('/login');
const value = ref('Войти');

fetch('http://localhost:5000/logout');
localStorage.removeItem('jwt_token');
    
function changePswd() {
  path.value = '/password',
  attr.value = 'alert-info',
  text.value = 'Заполните обязательные поля',
  title.value = 'Изменение пароля'
  value.value = 'Изменить'
}

async function submitData(event: Event) {
  try {
    const formData = new FormData(event.target as HTMLFormElement);
    const response = await axios.post(`http://localhost:5000/${path.value}`, formData);        
    const { user, access_token } = response.data;
    const alerts: Record<string, any> = {
      'None': ['alert-danger', 'Неверный логин или пароль'],
      'Overdue': ['alert-warning', 'Пароль просрочен. Измените пароль'],
      'Denied': ['alert-danger', 'Пользователь не авторизован'],
      'Not_match': ['alert-warning', 'Введенные пароли не совпадают'],
      'Success': ['alert-success', 'Пароль установлен. Войдите с новым паролем'],
      'Authorized': ['alert-success', 'Вы успешно авторизованы']
    };
    attr.value = alerts[user][0];
    text.value = alerts[user][1];
    if (user === "Success"){
      path.value = '/login';
      title.value = 'Вход в систему';
      value.value = 'Войти';
    } else if (user === "Authorized"){
      localStorage.setItem('jwt_token', access_token);
      router.push({ name: 'index', params: { flag: 'new' } });
    } else {
      console.log(user);
    }
  } catch (error) {
    console.log(error);
  }
}
    
</script>
