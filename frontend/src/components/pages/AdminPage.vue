<script setup lang="ts">

import { onBeforeMount } from 'vue'
import { storeAdmin } from '@store/admin';
import UserForm from '@content/forms/UserForm.vue';

const adminStore = storeAdmin();

onBeforeMount(async () => {
  adminStore.getUsers()
});

</script>

<template>
  <div class="container py-3">
    <div class="py-3">
      <h4>{{ adminStore.action === 'create' ? 'Добавить пользователя' : 'Список пользователей'}}</h4>
    </div>
    <UserForm v-if="adminStore.action === 'create'" />
    <div v-else class="py-2">
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
          <tr height="50px" v-for="user in adminStore.users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.fullname }}</td>
            <td>
              <router-link :to="{ name: 'shape', params: { group: 'admins', id: user.id} }">
                {{ user.username }}</router-link>
            </td>
            <td>{{ new Date(user.pswd_create).toLocaleString('ru-RU') }}</td>
            <td>{{ new Date(user.last_login).toLocaleString('ru-RU') }}</td>
          </tr>
        </tbody>
      </table>
      <div class="py-1">
        <button class="btn btn-primary" @click="adminStore.action = 'create'">Добавить пользователя</button>
      </div>
    </div>
  </div>
</template>