<script setup lang="ts">
// Компонент страницы профиля пользователя

import { computed, onBeforeMount } from 'vue';
import { appLocation } from '@store/location';
import { appUsers } from '@store/users';
import { useRoute } from 'vue-router';
import UserForm from '@content/forms/UserForm.vue'

const route = useRoute();

const storeUsers = appUsers();

const storeLocation = appLocation();

storeUsers.userId = route.params.id as string;  // ID пользователя из роута 


// Инициализация данных пользователя
onBeforeMount(async () => {
  storeUsers.viewUser();
});


const isBlocked = computed(() => {
  return storeUsers.profile.blocked ? 'Заблокирован' : 'Разблокирован';
});

</script>

<template>
  <div class="container py-3">
    <div class="py-5"><h4>Профиль пользователя</h4></div>
    <UserForm v-if="storeUsers.action === 'edit'" />
    <div v-else class="py-2">
      <table class="table table-responsive">
        <thead>
          <tr><th colspan="2"># {{ storeUsers.profile.id }}</th></tr>
        </thead>
        <tbody>
          <tr><td width="35%">Имя пользователя</td><td>{{storeUsers.profile.fullname }}</td></tr>
          <tr><td>Логин</td><td>{{ storeUsers.profile.username }}</td></tr>
          <tr><td>E-mail</td><td>{{ storeUsers.profile.email }}</td></tr>
          <tr><td>Регион</td><td>{{ storeLocation.regionsObject[storeUsers.profile.region_id as string] }}</td></tr>
          <tr><td>Создан</td><td>{{ new Date(storeUsers.profile.pswd_create).toLocaleString('ru-RU') }}</td></tr>
          <tr><td>Изменен</td><td>{{ new Date(storeUsers.profile.pswd_change).toLocaleString('ru-RU') }}</td></tr>
          <tr><td>Вход</td><td>{{ new Date(storeUsers.profile.last_login).toLocaleString('ru-RU')}}</td></tr>
          <tr><td>Роль</td><td>{{ storeUsers.profile.role }}</td></tr>
          <tr><td>Попыток входа</td><td>{{ storeUsers.profile.attempt }}</td></tr>
          <tr><td>Блокировка</td><td>{{ isBlocked }}</td></tr>
        </tbody>
      </table>
      <div class="btn-group py-2" role="group">
        <button @click="storeUsers.editUserInfo('block')" class="btn btn-outline-primary">
          {{storeUsers.profile.blocked ? "Разблокировать" : 'Заблокировать' }}
        </button>
        <button @click="storeUsers.action = 'edit'" class="btn btn-outline-primary">Редактировать</button>
        <button @click="storeUsers.editUserInfo('drop')" class="btn btn-outline-primary">Сбросить пароль</button>
        <button @click="storeUsers.editUserInfo('delete')" class="btn btn-outline-primary">Удалить</button>
      </div>
    </div>
  </div>
</template>