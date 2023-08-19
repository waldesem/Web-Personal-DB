<script setup lang="ts">
/* Компонент NavBar - выводит навигационную панель в шапке сайта для авторизованного пользователя.
Запускает интервал обновления сообщений и отображает ссылку на сообщения. 
Содержит ссылки на страницы: Кандидаты, Создать, Информация */

import axios from 'axios';
import { onMounted, ref } from 'vue';
import { appAuth } from '@/store/auth';
import { appUsers } from '@/store/userinfo';
import server from '@store/server';
import router from '@router/router';

const storeAuth = appAuth();

const storeUsers = appUsers();

const messages = ref([]);  // Список сообщений для пользователя

let isStarted = false;  // Флаг  для проверки запуска интервала обновления


// Получение списка сообщений после монтирования компонента и обновление каждые 10 минут
onMounted(async () => {
  if (!isStarted) {
    isStarted = true;
    setInterval(updateMessage, 1800000);
  }
});


/**
 * Updates the messages based on the provided flag ('new' or 'reply').
 *
 * @param {string} flag - The flag to determine which messages to update. Default is 'new'.
 * @return {Promise<void>} - A promise that resolves when the message is successfully updated.
 */
async function updateMessage(flag: string = 'new'): Promise<void> {
  try{
    const response = await storeAuth.axiosInstance.get(`${server}/messages/${flag}`);
    messages.value = response.data;
    
  } catch (error) {
    console.error(error);
  }
}


/**
 * Logs the user out by sending a DELETE request to the server's logout endpoint.
 *
 * @return {Promise<void>} Promise that resolves when the user is successfully logged out.
 */
async function userLogout(): Promise<void>{
  const response = await storeAuth.axiosInstance.delete(`${server}/logout`);
  console.log(response.status);

  const resp = await axios.delete(`${server}/logout`, {
    headers: {'Authorization': `Bearer ${localStorage.getItem('refresh_token')}`}
  });
  console.log(resp.status);

  
  // Удаление токенов для авторизации и редирект на страницу авторизации
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');

  router.push({ name: 'login' });
}

</script>


<template>
  <div class="container-fluid">
    <nav class="navbar navbar-expand navbar-nav mr-auto navbar-dark bg-primary">
      <div class="container">
        <router-link :to="{ name: 'app'}" class="nav-link active">StaffSec</router-link>
        <div class="navbar-nav mr-auto collapse navbar-collapse" id="navbarContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link :to="{ name: 'persons'}" class="nav-link active">Кандидаты</router-link>
            </li>
            <li class="nav-item">
              <router-link :to="{ name: 'resume' }" class="nav-link active">Создать</router-link>
            </li>
            <li class="nav-item">
              <router-link :to="{ name: 'information' }" class="nav-link active">Информация</router-link>
            </li>
            <li v-if="messages.length" class="nav-item dropdown">
              <a class="nav-link active dropdown-toggle dropdown-toggle-split" role="button" data-bs-toggle="dropdown" href="#"><i class="bi bi-envelope-fill"></i>
                <span class="position-absolute translate-middle badge rounded-pill text-bg-success">{{messages ? messages.length : 0}}</span></a>
                <ul class="dropdown-menu">
                  <h6 class="dropdown-header">Непрочитанные сообщения</h6>
                  <li v-for="message in messages" :key="message['id']">
                    <a class="dropdown-item">{{ `${new Date(message['create']).toLocaleString('ru-RU')}: ${message['message']}` }}</a>
                  </li>
                  <div class="dropdown-divider"></div>
                  <li><a class="dropdown-item" href="#" @click="updateMessage('reply')">Очистить</a></li>
                </ul>
            </li>
            <li v-else class="nav-item"><a class="nav-link" title="Сообщения" href="#"><i class="bi bi-envelope"></i></a></li>
          </ul>                                
          <li class="nav-item dropdown d-flex">
            <a href="#" class="nav-link active dropdown-toggle" role="button" data-bs-toggle="dropdown" :title="storeUsers.fullName">
              {{ storeUsers.fullName.split(' ').map(item => item.charAt(0)).join('') }}
              <i class="bi bi-person-circle"></i>
            </a>
            <ul class="dropdown-menu">
              <li><a class="dropdown-item" href="#" @click="userLogout">Выход</a></li>
            </ul>
          </li>
        </div>
      </div>
    </nav>
  </div>
</template>

<style>
  .envelope {
    font-size: 2rem; /* Adjust the value as needed */
  }
</style>