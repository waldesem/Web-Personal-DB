<template>
  <router-view></router-view>
  <div class="container px-5 py-5">
    <div class="border border-primary px-5 py-5">
      <AlertMessage :attr="data.attr" :text="data.text" />
      <h5>{{data.title}}</h5>
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
                    <div v-if="data.path ==='/login'" class="py-2"><a @click="changePswd" href="#">Изменить пароль</a></div>
                  </div>
              </div>
          <div v-if="data.path === '/password'">
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
                  <button class="btn btn-primary btn-md" name="submit" type="submit">{{ data.value }}</button>
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
import appUrl from '@/main';
import router from '../router';
import AlertMessage from './AlertMessage.vue';

const data = ref({
  attr: 'alert-info',
  text: 'Авторизуйтесь для входа в систему',
  title: 'Вход в систему',
  path: '/login',
  value: 'Войти'
});

fetch(`${appUrl}/logout`);
localStorage.removeItem('jwt_token');
    
function changePswd() {
  Object.assign(data.value, {
    attr: 'alert-info',
    text: 'Заполните обязательные поля',
    title: 'Изменение пароля',
    path: '/password',
    value: 'Изменить'
  })
}

async function submitData(event: Event) {
  try {
    const formData = new FormData(event.target as HTMLFormElement);
    const response = await axios.post(`${appUrl}/${data.value.path}`, formData);        
    const { user, access_token } = response.data;
    const alerts: Record<string, any> = {
      'None': ['alert-danger', 'Неверный логин или пароль'],
      'Overdue': ['alert-warning', 'Пароль просрочен. Измените пароль'],
      'Denied': ['alert-danger', 'Пользователь не авторизован'],
      'Not_match': ['alert-warning', 'Введенные пароли не совпадают'],
      'Success': ['alert-success', 'Пароль установлен. Войдите с новым паролем'],
      'Authorized': ['alert-success', 'Вы успешно авторизованы']
    };
    Object.assign(data.value, {
      attr: alerts[user][0],
      text: alerts[user][1],
    })
    if (user === "Success"){
      Object.assign(data.value, {
        path: '/login',
        title: 'Вход в систему',
        value: 'Войти'
      })
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
