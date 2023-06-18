<template>
  <div class="container-fluid">
    <nav class="navbar navbar-expand navbar-nav mr-auto navbar-dark bg-primary">
      <div class="container">
        <router-link :to="{ name: 'index', params: {flag: 'main'} }" class="nav-link active">StaffSec</router-link>
        <div class="navbar-nav mr-auto collapse navbar-collapse" id="navbarContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link :to="{ name: 'index', params: {flag: 'new'} }" class="nav-link active">Кандидаты
                <span class="position-absolute translate-middle badge rounded-pill text-bg-success">{{now}}</span></router-link>
            </li>
            <li class="nav-item">
              <router-link :to="{ name: 'profile', params: {id: '0'}}" class="nav-link active">Создать</router-link>
            </li>
            <li class="nav-item">
              <router-link :to="{ name: 'index', params: {flag: 'officer'} }" class="nav-link active">Кабинет
                <span class="position-absolute translate-middle badge rounded-pill text-bg-success">{{usr}}</span></router-link>
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

const now = ref('');
const usr = ref('');

(async (): Promise<void> => {
  try {
    const response = await axios.get('http://localhost:5000/count', {
      headers: {'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`
    }});
    const { news, checks } = response.data;
    now.value = news;
    usr.value = checks
  } catch (error) {
    console.log(error);
  }
})();

</script>