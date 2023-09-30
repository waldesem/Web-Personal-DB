<script setup lang="ts">

import { appMessages } from '@/store/messages';
import { appLogin } from '@/store/login';
import { appProfile } from '@/store/profile';

const storeMessages = appMessages();
const storeLogin = appLogin();
const storeProfile = appProfile();

</script>

<template>
  <nav v-if="!storeProfile.printPdf" :class="storeLogin.pageIdentity ==='admins' 
          ? 'navbar navbar-expand navbar-nav mr-auto navbar-dark bg-secondary' 
          : 'navbar navbar-expand navbar-nav mr-auto navbar-dark bg-primary'">
    <div class="container">
      <a class="navbar-brand" data-bs-toggle="offcanvas" href="#offcanvasMenu">
        {{ storeLogin.pageIdentity ? storeLogin.pageIdentity.toUpperCase() : '' }}</a>
      <div class="navbar-nav mr-auto collapse navbar-collapse" id="navbarContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          
          <template v-if="storeLogin.pageIdentity === 'admins'">
            <li class="nav-item">
              <router-link :to="{ name: 'users', params: { group: 'admins' } }" 
                  class="nav-link active" href="#">
                Пользователи</router-link>
            </li>
            <li class="nav-item">
              <router-link :to="{ name: 'table', params: { group: 'admins' } }" 
                  class="nav-link active" href="#">
                Таблицы</router-link>
            </li>
          </template>

          <template v-if="storeLogin.pageIdentity === 'staffsec'">
            <li class="nav-item">
                <router-link :to="{ name: 'persons', params: { group: 'staffsec' }}" 
                    class="nav-link active">
                  Кандидаты</router-link>
            </li>
            <li class="nav-item">
                <router-link :to="{ name: 'resume', params: { group: 'staffsec' } }" 
                    class="nav-link active">
                  Создать</router-link>
            </li>
            <li class="nav-item">
                <router-link :to="{ name: 'information', params: { group: 'staffsec' } }" 
                    class="nav-link active">
                  Информация</router-link>
            </li>
          </template>

          <li v-if="!['login', 'admins', undefined].includes(storeLogin.pageIdentity)" class="nav-item">
            <router-link :to="{name: 'contacts', params: { group: 'staffsec' }}" 
                class="nav-link active">
              Контакты</router-link>
          </li>

          <li v-if="storeMessages.messages.length && storeLogin.pageIdentity !== 'login'" 
              class="nav-item dropdown">
            <a class="nav-link active dropdown-toggle" role="button" data-bs-toggle="dropdown" href="#">
              <i class="bi bi-envelope-fill"></i>
              <span class="position-absolute translate-middle badge rounded-pill text-bg-success">
                {{ storeMessages.messages.length }}
              </span>
            </a>
              <ul class="dropdown-menu">
                <h6 class="dropdown-header">Новые сообщения</h6>
                <li v-for="message in storeMessages.messages" :key="message['id']">
                  <a class="dropdown-item">
                    <p>{{ `${new Date(message['create']).toLocaleString('ru-RU')}:`}}</p>
                    <p>{{ message['report'] }}</p>
                  </a>
                </li>
                <div class="dropdown-divider"></div>
                <li>
                  <a class="dropdown-item" href="#" 
                    @click="storeMessages.updateMessage('reply')">Очистить</a>
                </li>
              </ul>
          </li>
        </ul>                                
        <li class="nav-item dropdown d-flex">
          <a href="#" class="nav-link active dropdown-toggle" role="button" 
              data-bs-toggle="dropdown" :title="storeLogin.userData.fullName 
                  ? storeLogin.userData.fullName : ''">
            {{ storeLogin.userData.fullName 
                ? storeLogin.userData.fullName.split(' ').map(item => item.charAt(0)).join('') 
                : '' }}
            <i class="bi bi-person-circle"></i>
          </a>
          <ul class="dropdown-menu">
            <li>
              <a class="dropdown-item" href="#" @click="storeLogin.userLogout">Выход</a>
            </li>
          </ul>
        </li>
      </div>
    </div>
  </nav>

  <div class="offcanvas offcanvas-start" tabindex="-1" id="offcanvasMenu">
    <div class="offcanvas-header">
      <h5 class="offcanvas-title" id="offcanvasLabel">Деператамент экономической безопасности</h5>
    </div>
    <div class="offcanvas-body">
        <ul>
          <li v-if="storeLogin.hasGroup('admins')" class="mb-4">
            <router-link :to="{ name: 'users', params: { group: 'admins' } }">
              Администраторы</router-link>
          </li>
          <li class="mb-4">
            <router-link v-if="storeLogin.hasGroup('staffsec')" 
                :to="{ name: 'persons', params: { group: 'staffsec' } }">
              Центр кадровой безопасности</router-link>
            <p v-else>Центр кадровой безопасности</p>
          </li>
        </ul>
    </div>
  </div>
</template>

<style>
  .envelope {
    font-size: 2rem; /* Adjust the value as needed */
  }
  .dropdown-menu {
    max-width: 1000px;
    max-height: 1000px; /* set a fixed height for the dropdown menu */
    overflow-y: auto; /* enable vertical scrolling */
    overflow-x: auto  ;
  }
</style>