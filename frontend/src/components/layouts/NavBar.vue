<script setup lang="ts">
/* Компонент NavBar - выводит навигационную панель в шапке сайта для авторизованного пользователя.
Содержит ссылки на страницы: Кандидаты, Создать, Информация */

import { appPersons } from '@/store/persons';
import { appLogin } from '@/store/login';


const personsStore = appPersons();
const storeLogin = appLogin();

</script>

<template>
  <div class="container-fluid">
    <nav class="navbar navbar-expand navbar-nav mr-auto navbar-dark bg-primary">
      <div class="container">
        <a class="navbar-brand" href="#">StaffSec</a>
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
            <li v-if="personsStore.messages.length" class="nav-item dropdown">
              <a class="nav-link active dropdown-toggle" role="button" data-bs-toggle="dropdown" href="#"><i class="bi bi-envelope-fill"></i>
                <span class="position-absolute translate-middle badge rounded-pill text-bg-success">{{personsStore.messages ? personsStore.messages.length : 0}}</span></a>
                <ul class="dropdown-menu">
                  <h6 class="dropdown-header">Непрочитанные сообщения</h6>
                  <li v-for="message in personsStore.messages" :key="message['id']">
                    <a class="dropdown-item">{{ `${new Date(message['create']).toLocaleString('ru-RU')}: ${message['report']}` }}</a>
                  </li>
                  <div class="dropdown-divider"></div>
                  <li><a class="dropdown-item" href="#" @click="personsStore.updateMessage('reply')">Очистить</a></li>
                </ul>
            </li>
          </ul>                                
          <li class="nav-item dropdown d-flex">
            <a href="#" class="nav-link active dropdown-toggle" role="button" data-bs-toggle="dropdown" :title="storeLogin.fullName">
              {{ storeLogin.fullName.split(' ').map(item => item.charAt(0)).join('') }}
              <i class="bi bi-person-circle"></i>
            </a>
            <ul class="dropdown-menu">
              <li><a class="dropdown-item" href="#" @click="storeLogin.userLogout">Выход</a></li>
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