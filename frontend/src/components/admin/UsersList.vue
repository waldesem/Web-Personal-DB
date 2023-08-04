<script setup lang="ts">

import { ref, onBeforeMount } from 'vue'
import axios from 'axios';
import config from '../../config';
import AlertMessage from '../AlertMessage.vue';
import FooterDiv from '../FooterDiv.vue';
import NavbarAdmin from './NavbarAdmin.vue'
import UserForm from './UserForm.vue';



const data = ref({
  users: [],
  attr: '',
  text: ''
});


onBeforeMount(async () => {
  getUsers()
});


async function getUsers(){
  try {
    const response = await axios.get(`${config.appUrl}/admin/users`, {
      headers: {'Authorization': `Bearer ${localStorage.getItem('access_token')}`}
    });
    data.value.users = response.data;
  } catch (error) {
    console.error(error);
  }
};

</script>


<template>
  <NavbarAdmin />
  <div class="container py-5">
    <AlertMessage v-if="data.attr" :attr="data.attr" :text="data.text" />
    <div class="py-5"><h4>Список пользователей</h4></div>
      <UserForm :action="'create'" :userId="'0'" />
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
          <tr height="50px" v-for="user in data.users" :key="user">
            <td>{{ user["id" as keyof typeof user] }}</td>
            <td>{{ user["fullname" as keyof typeof user] }}</td>
            <td><router-link :to="{ name: 'shape', params: {flag: 'id'} }" href="#">{{ user["username" as keyof typeof user] }}</router-link></td>
            <td>{{ new Date(user["pswd_create" as keyof typeof user]).toLocaleString('ru-RU') }}</td>
            <td>{{ new Date(user["last_login" as keyof typeof user]).toLocaleString('ru-RU') }}</td>
            <td>{{ user["role" as keyof typeof user] }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  <FooterDiv />
</template>