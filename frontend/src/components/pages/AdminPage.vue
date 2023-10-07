<script setup lang="ts">

import { onBeforeMount } from 'vue';
import { onBeforeRouteLeave } from 'vue-router';
import { adminStore } from '@store/admin';
import UserContent from '@content/UserContent.vue';

const storeAdmin = adminStore();

onBeforeMount(async () => {
  storeAdmin.getUsers()
});

onBeforeRouteLeave((_to: any, _from: any, next: () => void) => {
  Object.assign(storeAdmin.userData, {
    userList: [],
    userId: '',
    userAct: '',
    userFlag: '',
    userRole: '',
    userGroup: '',
    currentPage: 1,
    hasNext: false,
    hasPrev: false,
  });

  Object.assign(storeAdmin.profileData, {
    id: '',
    fullname: '',
    region_id: '',
    username: '',
    email: '',
    pswd_create: '',
    pswd_change: '',
    last_login: '',
    roles: [],
    groups: [],
    blocked: '',
    attempt: ''
  });
  next();
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
                @click="storeAdmin.userAction('view', user.id)" >
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
