<script setup lang="ts">

import { onBeforeMount } from 'vue';
import { adminStore } from '@store/admin';
import { debounce } from '@share/utilities';
import HeaderDiv from '@components/layouts/HeaderDiv.vue';
import UserForm from '@components/forms/UserForm.vue';

const storeAdmin = adminStore();


onBeforeMount(async () => {
  storeAdmin.getUsers()
});

const searchUsers = debounce(storeAdmin.getUsers, 500);


</script>

<template>
  <div class="container py-3">
    <HeaderDiv :page-header="'Список пользователей'" />
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
                <router-link :to="{ name: 'user', params: { id: user.id } }">
                  {{ user.username }}
                </router-link>
              </td>
              <td width="20%">{{ new Date(user.pswd_create).toLocaleString('ru-RU') }}</td>
              <td width="20%">{{ new Date(user.last_login).toLocaleString('ru-RU') }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <UserForm />
  </div>
</template>

<style scoped>
.overflow {
  height: 75vh;
  overflow-y: auto;
}
</style>