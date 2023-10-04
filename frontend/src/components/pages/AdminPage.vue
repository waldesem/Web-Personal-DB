<script setup lang="ts">

import { onBeforeMount } from 'vue'
import { adminStore } from '@store/admin';
import UserContent from '@content/UserContent.vue';

const storeAdmin = adminStore();

onBeforeMount(async () => {
  storeAdmin.getUsers()
});

</script>

<template>
  <div class="container py-3">
    <div class="py-3">
      <h4>{{ storeAdmin.userData.userAct === 'create' 
        ? 'Добавить пользователя' 
        : 'Список пользователей'}}
      </h4>
    </div>
    <UserContent />
    <div class="py-2">
      <table class="table table-responsive align-middle">
        <thead>
          <tr height="50px">
            <th width="5%">#</th>
            <th>Имя пользователя</th>
            <th width="25%">Логин</th>
            <th width="20%">Создан</th>
            <th width="20%">Вход</th>
          </tr>
        </thead>
        <tbody>
          <tr height="50px" v-for="user in storeAdmin.userData.userList" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.fullname }}</td>
            <td>
              <a href="#" data-bs-toggle="modal" data-bs-target="#modalUser"
                    @click="storeAdmin.userData.userId=user.id" >
                {{ user.username }}</a>
            </td>
            <td>{{ new Date(user.pswd_create).toLocaleString('ru-RU') }}</td>
            <td>{{ new Date(user.last_login).toLocaleString('ru-RU') }}</td>
          </tr>
        </tbody>
      </table>
      <div class="py-1">
        <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#modalUser"
                @click="storeAdmin.userData.userAct = 'create'">
          Добавить пользователя
        </button>
      </div>
    </div>
  </div>
</template>