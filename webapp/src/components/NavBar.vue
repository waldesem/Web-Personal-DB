<template>
  <div class="container-fluid">
    <nav class="navbar navbar-expand navbar-nav mr-auto navbar-dark bg-primary">
      <div class="container">
        <router-link :to="{ name: 'index', params: {flag: 'main'} }" class="nav-link active">StaffSec</router-link>
        <div class="navbar-nav mr-auto collapse navbar-collapse" id="navbarContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link :to="{ name: 'index', params: {flag: 'new'} }" class="nav-link active">Кандидаты
                <span class="position-absolute translate-middle badge rounded-pill text-bg-success">{{data.now}}</span></router-link>
            </li>
            <li class="nav-item">
              <router-link :to="{ name: 'profile', params: {id: '0'}}" class="nav-link active">Создать</router-link>
            </li>
            <li class="nav-item">
              <router-link :to="{ name: 'index', params: {flag: 'officer'} }" class="nav-link active">Кабинет
                <span class="position-absolute translate-middle badge rounded-pill text-bg-success">{{data.usr}}</span></router-link>
            </li>
            <li class="nav-item">
              <router-link :to="{ name: 'information' }" class="nav-link active">Информация</router-link>
            </li>
          </ul>                                
        </div>                        
        <div class="d-flex px-2">
          <router-link :to="{name: 'login'}" class="nav-link active">Выход</router-link>
        </div>
      </div>
    </nav>
  </div>
</template>

<script setup lang="ts">

import axios from 'axios';
import { ref } from 'vue';
import appUrl from '@/main';

const data = ref({now: '', usr: ''});

(async (): Promise<void> => {
  try {
    const response = await axios.get(`${appUrl}/count`, {
      headers: {'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`
    }});
    const { news, checks } = response.data;
    Object.assign(data.value, {now: news, usr: checks});
  } catch (error) {
    console.log(error);
  }
})();

</script>