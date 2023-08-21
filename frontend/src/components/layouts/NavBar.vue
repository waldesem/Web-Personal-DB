<script setup lang="ts">
/* Компонент NavBar - выводит навигационную панель в шапке сайта для авторизованного пользователя.
Запускает интервал обновления сообщений и отображает ссылку на сообщения. 
Содержит ссылки на страницы: Кандидаты, Создать, Информация */

import { NavigationBar } from '@/store/navbar';
import { appLogin } from '@/store/login';


const storeNavbar = NavigationBar();

const storeLogin = appLogin();

</script>

<template>
  <div class="container-fluid">
    <nav class="navbar navbar-expand navbar-nav mr-auto navbar-dark bg-primary">
      <div class="container">
        <router-link :to="{ name: 'app'}" class="nav-link active">StaffSec</router-link>
        <!--a class="btn btn-primary" data-bs-toggle="offcanvas" href="#offcanvasMenu" role="button">Link with href</a-->
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
            <li v-if="storeNavbar.messages.length" class="nav-item dropdown">
              <a class="nav-link active dropdown-toggle dropdown-toggle-split" role="button" data-bs-toggle="dropdown" href="#"><i class="bi bi-envelope-fill"></i>
                <span class="position-absolute translate-middle badge rounded-pill text-bg-success">{{storeNavbar.messages ? storeNavbar.messages.length : 0}}</span></a>
                <ul class="dropdown-menu">
                  <h6 class="dropdown-header">Непрочитанные сообщения</h6>
                  <li v-for="message in storeNavbar.messages" :key="message['id']">
                    <a class="dropdown-item">{{ `${new Date(message['create']).toLocaleString('ru-RU')}: ${message['message']}` }}</a>
                  </li>
                  <div class="dropdown-divider"></div>
                  <li><a class="dropdown-item" href="#" @click="storeNavbar.updateMessage('reply')">Очистить</a></li>
                </ul>
            </li>
            <li v-else class="nav-item"><a class="nav-link" title="Сообщения" href="#"><i class="bi bi-envelope"></i></a></li>
          </ul>                                
          <li class="nav-item dropdown d-flex">
            <a href="#" class="nav-link active dropdown-toggle" role="button" data-bs-toggle="dropdown" :title="storeLogin.fullName">
              {{ storeLogin.fullName.split(' ').map(item => item.charAt(0)).join('') }}
              <i class="bi bi-person-circle"></i>
            </a>
            <ul class="dropdown-menu">
              <li><a class="dropdown-item" href="#" @click="storeNavbar.userLogout">Выход</a></li>
            </ul>
          </li>
        </div>
      </div>
    </nav>
  </div>

  <!--div class="offcanvas offcanvas-start" tabindex="-1" id="offcanvasMenu" aria-labelledby="offcanvasMenuLabel">
    <div class="offcanvas-header">
      <h5 class="offcanvas-title" id="offcanvasExampleLabel">Offcanvas</h5>
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>
    <div class="offcanvas-body">
      <div>
        Some text as placeholder. In real life you can have the elements you have chosen. Like, text, images, lists, etc.
      </div>
      <div class="dropdown mt-3">
        <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown">
          Dropdown button
        </button>
        <ul class="dropdown-menu">
          <li><a class="dropdown-item" href="#">Action</a></li>
          <li><a class="dropdown-item" href="#">Another action</a></li>
          <li><a class="dropdown-item" href="#">Something else here</a></li>
        </ul>
      </div>
    </div>
  </div-->

</template>

<style>
  .envelope {
    font-size: 2rem; /* Adjust the value as needed */
  }
</style>