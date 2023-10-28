<script setup lang="ts">

import { watch, ref } from 'vue';
import { authStore } from '@/store/token';
import { loginStore } from '@/store/login';
import { profileStore } from '@/store/profile';
import { adminStore } from '@/store/admin';
import { socketStore } from '@store/socket'
import { server } from '@share/utilities';

const storeAuth = authStore();
const storeLogin = loginStore();
const storeProfile = profileStore();
const storeAdmin = adminStore();
const storeSocket = socketStore();

const textInput  = ref('');

watch(() => storeSocket.chatDialog, () => {
  scrollToBottom();
})

function scrollToBottom() {
  const chatbot = document.getElementById('chatbot');
  const chatcontent = document.getElementById('chatcontent');
  if (chatcontent && chatbot) {
    chatcontent.scrollTop = chatcontent.scrollHeight + chatbot.scrollHeight;
  }
};

function updateChat() {
  storeSocket.chatDialog.push({'Вы': textInput.value});
  storeSocket.socket.emit("income", {'Вы': textInput.value});
  textInput.value = '';
};

const messages = ref([]);

let isStarted = false;
if (!isStarted) {
  updateMessage();
  isStarted = true;
  setInterval(updateMessage, 1000000);
};

/**
 * Updates the messages based on the provided flag ('new' or 'reply').
 *
 * @param {string} flag - The flag to determine which messages to update. Default is 'new'.
 * @return {Promise<void>} - A promise that resolves when the message is successfully updated.
 */
async function updateMessage(flag: string = 'new'): Promise<void> {
  try {
    const response = flag === 'new' 
      ? await storeAuth.axiosInstance.get(`${server}/messages`)
      : await storeAuth.axiosInstance.delete(`${server}/messages`);
    messages.value = response.data;
      
  } catch (error) {
    console.error(error);
  }
};

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
              <router-link :to="{ name: 'table', params: { group: 'admins' } }" class="nav-link active" href="#">
                Таблицы
              </router-link>
            </li>
          </template>

          <template v-if="storeLogin.pageIdentity === 'staffsec'">
            <li class="nav-item">
                <router-link :to="{ name: 'persons', params: { group: 'staffsec' }}" class="nav-link active">
                  Кандидаты
                </router-link>
            </li>
            <li class="nav-item">
                <router-link :to="{ name: 'resume', params: { group: 'staffsec' } }" class="nav-link active">
                  Создать
                </router-link>
            </li>
            <li class="nav-item">
                <router-link :to="{ name: 'information', params: { group: 'staffsec' } }" class="nav-link active">
                  Информация
                </router-link>
            </li>
          </template>

          <li v-if="!['login', 'admins', undefined].includes(storeLogin.pageIdentity)" 
                class="nav-item">
            <router-link :to="{name: 'contacts', params: { group: 'staffsec' }}" class="nav-link active">
              Контакты
            </router-link>
          </li>

          <li v-if="messages.length && storeLogin.pageIdentity !== 'login'" 
              class="nav-item dropdown" title="Сообщения">
            <a class="nav-link active dropdown-toggle" role="button" data-bs-toggle="dropdown" href="#">
              <i class="bi bi-envelope-fill"></i>
              <span class="position-absolute translate-middle badge rounded-pill text-bg-success">
                {{ messages.length }}
              </span>
            </a>
              <ul class="dropdown-menu" id="messages">
                <h6 class="dropdown-header">Новые сообщения</h6>
                <li v-for="message in messages" :key="message['id']">
                  <a class="dropdown-item">
                    <p>{{ `${new Date(message['create']).toLocaleString('ru-RU')}:`}}</p>
                    <p>{{ message['report'] }}</p>
                  </a>
                </li>
                <div class="dropdown-divider"></div>
                <li>
                  <a class="dropdown-item" href="#" 
                    @click="updateMessage('reply')">Очистить</a>
                </li>
              </ul>
          </li>

          <li class="nav-item dropdown" title="ChatBot">
            <div class="container">
              <a class="nav-link active dropdown-toggle" role="button"  
                data-bs-toggle="dropdown" data-bs-auto-close="false">
                <i class="bi bi-chat-dots-fill"></i>
              </a>
              <div class="dropdown-menu" id="chatbot">
                <p class="dropdown-header text-center fs-5">StaffSecBot</p>
                <hr class="dropdown-divider">
                <div id="chatcontent">
                  <div v-for="dialog, index in storeSocket.chatDialog" :key="index" 
                      :class="`${Object.keys(dialog)[0] === 'chatBot' ? 'px-3' : 'px-5'} py-2`">
                    <div :class="`p-3 bg-${Object.keys(dialog)[0] !== 'chatBot' ? 'danger' : 'success'} bg-opacity-75 border rounded text-wrap text-light`">
                      {{ `${Object.keys(dialog)[0]}: ${Object.values(dialog)[0]}` }}
                    </div>
                  </div>
                </div>
                <div class="py-3">
                  <form @submit.prevent="updateChat" class="form form-check" role="form">
                    <div class="row">
                      <div class="col-md-9">
                        <input class="form-control" id="chat" name="chat" required v-model="textInput">
                      </div>
                      <div class="col-md-1">
                        <button class="btn btn-outline-primary" type="submit">Отправить</button>
                      </div>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </li>

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

  #chatbot{
    width: 640px;
    height: 640px;
  }

  #chatcontent
  { 
    width: 620px;
    height: 480px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
  }
</style>