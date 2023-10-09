<script setup lang="ts">

import { onBeforeMount } from 'vue';
import { adminStore } from '@store/admin';
import { debounce } from '@share/utilities';
import UserContent from '@components/content/UserContent.vue';

const storeAdmin = adminStore();

onBeforeMount(async () => {
  storeAdmin.getUsers()
});

const searchUsers = debounce(storeAdmin.getUsers, 500);

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
    <form @input="searchUsers" class="form form-check" role="form">
      <div class="row py-3">
        <input class="form-control" id="fullusername" name="fullusername" type="text" 
               v-model="storeAdmin.userData.searchUser">
      </div>
    </form>
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
      </table>
      <div class="overflow">
        <table class="table table-responsive align-middle" >
          <tbody>
            <tr height="50px" v-for="user in storeAdmin.userData.userList" :key="user.id">
              <td width="5%">{{ user.id }}</td>
              <td>{{ user.fullname }}</td>
              <td width="25%">
                <a href="#" data-bs-toggle="modal" data-bs-target="#modalUser"
                  @click="storeAdmin.userAction('view', user.id)" >
                  {{ user.username }}</a>
              </td>
              <td width="20%">{{ new Date(user.pswd_create).toLocaleString('ru-RU') }}</td>
              <td width="20%">{{ new Date(user.last_login).toLocaleString('ru-RU') }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="py-1">
        <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#modalUser"
                @click="storeAdmin.userData.userAct = 'create'">
          Добавить пользователя
        </button>
      </div>
    </div>
  </div>
</template>

<style>
.overflow {
  height: 300px;
  overflow-y: auto;
} 
</style>