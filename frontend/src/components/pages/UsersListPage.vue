<script setup lang="ts">

import { onBeforeMount } from 'vue'
import { appUsers } from '@/store/users';
import UserForm from '@content/forms/UserForm.vue';

const storeUsers = appUsers();

// Получение списка пользователей
onBeforeMount(async () => {
  storeUsers.getUsers()
});

</script>

<template>
  <div class="container py-5">
    <div class="py-3"><h4>{{ storeUsers.action === 'create' ? 'Добавить пользователя' : 'Список пользователей'}}</h4></div>
    <UserForm v-if="storeUsers.action === 'create'" />
    <div v-else class="py-2">
      <table class="table table-hover table-responsive align-middle">
        <thead>
          <tr height="50px">
            <th width="5%">#</th>
            <th>Имя пользователя</th>
            <th width="15%">Логин</th>
            <th width="20%">Создан</th>
            <th width="20%">Вход</th>
            <th width="10%">Роль</th>
          </tr>
        </thead>
        <tbody>
          <tr height="50px" v-for="user in storeUsers.users" :key="user['id' as keyof typeof user]">
            <td>{{ user["id" as keyof typeof user] }}</td>
            <td>{{ user["fullname" as keyof typeof user] }}</td>
            <td>
              <router-link 
                :to="{ name: 'shape', params: {id: user['id' as keyof typeof user]} }" 
                href="#">{{ user["username" as keyof typeof user]}}
              </router-link>
              </td>
            <td>{{ new Date(user["pswd_create" as keyof typeof user]).toLocaleString('ru-RU') }}</td>
            <td>{{ new Date(user["last_login" as keyof typeof user]).toLocaleString('ru-RU') }}</td>
            <td>{{ user["role" as keyof typeof user] }}</td>
          </tr>
        </tbody>
      </table>
      <button class="btn btn-primary" @click="storeUsers.action = 'create'">Добавить пользователя</button>
    </div>
  </div>
</template>