<script setup lang="ts">

import { watch } from 'vue';
import { useRoute } from 'vue-router';
import { loginStore } from '@/store/login';
import { adminStore } from '@/store/admin';
import { messageStore } from '@/store/messages';
import { timeSince } from '@share/utilities';

const storeLogin = loginStore();
const storeAdmin = adminStore();
const storeMessage = messageStore();
const route = useRoute();


let isStarted = false;

watch(() => route.params.group,
  newValue => {
    let updTimer = setInterval(storeMessage.updateMessages, 1000000);
    if (!isStarted && newValue && !['admins', 'login'].includes(newValue as string)) {
      isStarted = true;
      storeMessage.updateMessages();
      updTimer;
    } else {
      isStarted = false;
      clearInterval(updTimer)
    }
  });

</script>

<template>
  <nav :class="`navbar navbar-expand navbar-nav mr-auto navbar-dark d-print-none 
              ${storeLogin.pageIdentity ==='admins' ? 'bg-secondary' : 'bg-primary'}`">
    <div class="container">
      <a class="navbar-brand" data-bs-toggle="offcanvas" href="#offcanvasMenu">
        {{ storeLogin.pageIdentity ? storeLogin.pageIdentity.toUpperCase() : '' }}</a>
      <div class="navbar-nav mr-auto collapse navbar-collapse" id="navbarContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          
          <template v-if="storeLogin.pageIdentity === 'admins'">
            <li class="nav-item">
              <router-link :to="{ name: 'users', params: { group: 'admins' } }" class="nav-link active" href="#">
                Пользователи
              </router-link>
            </li>
            <li class="nav-item">
              <a class="nav-link active" href="#"
                data-bs-toggle="modal" data-bs-target="#modalUser"
                @click="storeAdmin.userData.userAct = 'create'">
                 Создать
              </a>
            </li>
            <li class="nav-item">
              <router-link :to="{ name: 'table', params: { group: 'admins' } }" 
                           class="nav-link active" href="#">
                Таблицы
              </router-link>
            </li>
          </template>

          <template v-if="storeLogin.pageIdentity === 'staffsec'">
            <li class="nav-item">
                <router-link :to="{ name: 'persons', params: { group: 'staffsec' }}" 
                             class="nav-link active">
                  Кандидаты
                </router-link>
            </li>
            <li class="nav-item">
                <router-link :to="{ name: 'resume', params: { group: 'staffsec' } }" 
                             class="nav-link active">
                  Создать
                </router-link>
            </li>
            <li class="nav-item">
                <router-link :to="{ name: 'information', params: { group: 'staffsec' } }" 
                             class="nav-link active">
                  Информация
                </router-link>
            </li>
            
            <li class="nav-item">
              <router-link :to="{name: 'contacts', params: { group: 'staffsec' }}"    
                           class="nav-link active">
              Контакты
              </router-link>
            </li>

            <li class="nav-item">
              <router-link :to="{ name: 'manager', params: { group: 'staffsec' } }" 
                           class="nav-link active" href="#">
                Файлы
              </router-link>
            </li>

            <li class="nav-item dropdown">
              <a class="nav-link active dropdown-toggle" role="button" data-bs-toggle="dropdown" href="#">
                Сообщения
                <span class="position-absolute translate-middle badge rounded-pill text-bg-success">
                  {{ storeMessage.messageData.messages.length }}
                </span>
              </a>
                <ul class="dropdown-menu" id="messages">
                  <h6 class="dropdown-header">Новые сообщения</h6>
                  <li v-for="message in storeMessage.messageData.messages" :key="message['id']">
                    <a class="dropdown-item">
                      <p>{{ timeSince(message['create']) }}</p>
                      <p>{{ message['report'] }}</p>
                    </a>
                  </li>
                  <div class="dropdown-divider"></div>
                  <li>
                    <router-link :to="{ name: 'messages', params: { group: 'staffsec' } }"
                                class="dropdown-item" >
                      Открыть сообщения
                    </router-link>
                  </li>
                </ul>
            </li>
          </template>
              
          <li class="nav-item">
            <a class="nav-link active" href="#" 
               data-bs-toggle="modal" data-bs-target="#modalApp" title="О программе">
               <i class="bi bi-exclamation-circle-fill" width="32" height="32"></i>
            </a>
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
      <h5 class="offcanvas-title" id="offcanvasLabel">
        Деператамент экономической безопасности
      </h5>
    </div>
    <div class="offcanvas-body">
        <ul>
          <li v-if="storeLogin.hasGroup('admins')" class="mb-4">
            <router-link :to="{ name: 'users', params: { group: 'admins' } }">
              Администраторы
            </router-link>
          </li>
          <li v-if="storeLogin.hasGroup('staffsec')" class="mb-4">
            <router-link :to="{ name: 'persons', params: { group: 'staffsec' } }">
              Центр кадровой безопасности
            </router-link>
          </li>
          <li v-else class="mb-4">
            <p>Центр кадровой безопасности</p>
          </li>
        </ul>
    </div>
  </div>

  <div class="modal fade" id="modalApp" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
      <div class="modal-content">
        <div class="modal-body py-5">
          <div class="text-primary text-opacity-75 py-3">
            <h1 class="text-center">StaffSec</h1>
          </div>
          <div class="text-secondary text-opacity-95 py-3">
            <h3 class="text-center">Кадровая безопасность</h3>
          </div>
          <div class="text-secondary text-opacity-95 py-3">
            <h5 class="text-center">Интерфейс базы данных кандидатов и сотрудников</h5>
          </div>
          <div class="progress" role="progressbar">
            <div class="progress-bar progress-bar-striped progress-bar-animated" 
                style="width: 100%"></div>
          </div>
          <div class="py-3">
            <p class="text-center text-secondary text-opacity-95 py-1">MIT License</p>
            <p class="text-center text-secondary text-opacity-95 py-1">2023 Версия 0.1</p>
          </div>
        </div>  
      </div>
    </div>
  </div>
  
</template>

<style scoped>

  #messages {
    max-width: 640px;
    max-height: 640px;
    overflow-y: auto;
    overflow-x: auto;
  }
  #messages::after {
    display: none;
  }

</style>