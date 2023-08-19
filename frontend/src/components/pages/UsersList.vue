<script setup lang="ts">

import { ref, onBeforeMount } from 'vue'
import { appAuth } from '@store/auth';
import server from '@store/server';
import UserForm from '@content/forms/UserForm.vue';

const storeAuth = appAuth()

const users = ref([]);  // Список пользователей

const action = ref(''); // Выбранное действие

// Получение списка пользователей
onBeforeMount(async () => {
  getUsers()
});

/**
 * Retrieves a list of users from the server.
 *
 * @return {Promise<void>} - A promise that resolves with the list of users retrieved from the server.
 */
async function getUsers(): Promise<void>{
  action.value = ''
  try {
    const response = await storeAuth.axiosInstance.get(`${server}/users`);
    users.value = response.data;
  
  } catch (error) {
    console.error(error);
  }
};

</script>


<template>
  <div class="container py-5">
    <div class="py-3"><h4>{{ action === 'create' ? 'Добавить пользователя' : 'Список пользователей'}}</h4></div>
    <UserForm v-if="action === 'create'" 
                  :action="action" 
                  @updateAction="getUsers" />
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
          <tr height="50px" v-for="user in users">
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
      <button class="btn btn-primary" @click="action = 'create'">Добавить пользователя</button>
    </div>
  </div>
</template>