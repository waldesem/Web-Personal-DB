<script setup lang="ts">

import { ref, onMounted } from 'vue';

import axios from 'axios';
import config from '@/config';

const data = ref({
  new: '', 
  message: []
});

async function updateMessage(flag = 'new') {
  try{
    const response = await axios.get(`${config.appUrl}/messages/${flag}`, {
      headers: {'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`}
    });
    data.value.message = response.data;
  } catch (error) {
    console.error(error);
  }
}

onMounted(async () => {
  try {
    const response = await axios.get(`${config.appUrl}/persons/new`, {
      headers: {'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`}
    });
    const { news } = response.data;
    data.value.new = news;
  } catch (error) {
    console.error(error);
  }
  updateMessage()
});

</script>

<template>
  <div class="container-fluid">
    <nav class="navbar navbar-expand navbar-nav mr-auto navbar-dark bg-primary">
      <div class="container">
        <router-link :to="{ name: 'index', params: {flag: 'main'} }" class="nav-link active">StaffSec</router-link>
        <div class="navbar-nav mr-auto collapse navbar-collapse" id="navbarContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link :to="{ name: 'index', params: {flag: 'new'} }" class="nav-link active">Кандидаты
                <span v-if="data.new" class="position-absolute translate-middle badge rounded-pill text-bg-info">{{data.new}}</span></router-link>
            </li>
            <li class="nav-item">
              <router-link :to="{ name: 'index', params: {flag: 'officer'} }" class="nav-link active">Кабинет</router-link>
            </li>
            <li class="nav-item">
              <router-link :to="{ name: 'profile', params: {id: '0'}}" class="nav-link active">Создать</router-link>
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
          <router-link :to="{name: 'login'}" class="nav-link active" data-bs-toggle="tooltip" data-bs-placement="right" title="Выход"><i class="bi bi-box-arrow-in-right"></i></router-link>
        </div>
      </div>
    </nav>
  </div>
</template>