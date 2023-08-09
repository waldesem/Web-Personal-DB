<script setup lang="ts">

import { ref } from 'vue';
import { appAuth } from '@/store/auth';
import server from '@store/server';
import router from '@router/router';

const storeAuth = appAuth();

const data = ref({
  new: '', 
  message: []
});


// onMounted(async () => {
//   setInterval(updateMessage, 600000);
// });


async function updateMessage(flag = 'new') {
  try{
    const response = await storeAuth.axiosInstance.get(`${server}/messages/${flag}`);
    data.value.message = response.data;
  } catch (error) {
    console.error(error);
  }
}


async function userLogout(){
  const response = await storeAuth.axiosInstance.delete(`${server}/logout`);
  console.log(response.status);
  
  const resp = await storeAuth.axiosInstance.delete(`${server}/logout`);
  console.log(resp.status)
  
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
            <li v-if="data.message.length" class="nav-item dropdown">
              <a class="nav-link active dropdown-toggle dropdown-toggle-split" role="button" data-bs-toggle="dropdown" href="#"><i class="bi bi-envelope-check-fill"></i>
                <span class="position-absolute translate-middle badge rounded-pill text-bg-success">{{data.message ? data.message.length : 0}}</span></a>
                <ul class="dropdown-menu">
                  <h6 class="dropdown-header">Непрочитанные сообщения</h6>
                  <li v-for="message in data.message" :key="message['id']">
                    <a class="dropdown-item">{{ `${new Date(message['create']).toLocaleString('ru-RU')}: ${message['message']}` }}</a>
                  </li>
                  <div class="dropdown-divider"></div>
                  <li><a class="dropdown-item" href="#" @click="updateMessage('reply')">Очистить</a></li>
                </ul>
            </li>
            <li v-else class="nav-item"><a class="nav-link" data-bs-toggle="tooltip" data-bs-placement="right" title="Сообщения" href="#"><i class="bi bi-envelope-fill"></i></a></li>
          </ul>                                
        </div>
        <div class="d-flex px-2">
          <a @click="userLogout" class="nav-link active" data-bs-toggle="tooltip" data-bs-placement="right" title="Выход"><i class="bi bi-box-arrow-in-right"></i></a>
        </div>
      </div>
    </nav>
  </div>
</template>