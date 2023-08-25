<script setup lang="ts">
// Компонент страницы профиля пользователя

import { computed, onBeforeMount } from 'vue';
import { appLocation } from '@store/location';
import { storeAdmin } from '@store/admin';
import { useRoute } from 'vue-router';
import UserForm from '@content/forms/UserForm.vue'

const route = useRoute();
const adminStore = storeAdmin();
const storeLocation = appLocation();

adminStore.userId = route.params.id as string;  // ID пользователя из роута 


// Инициализация данных пользователя
onBeforeMount(async () => {
  adminStore.viewUser();
});


const isBlocked = computed(() => {
  return adminStore.profile.blocked ? 'Заблокирован' : 'Разблокирован';
});

</script>

<template>
  <div class="container py-3">
    <div class="py-5"><h4>Профиль пользователя</h4></div>
    <UserForm v-if="adminStore.action === 'edit'" />
    <div v-else class="py-2">
      <table class="table table-responsive">
        <thead>
          <tr><th colspan="2"># {{ adminStore.profile.id }}</th></tr>
        </thead>
        <tbody>
          <tr><td width="35%">Имя пользователя</td><td>{{adminStore.profile.fullname }}</td></tr>
          <tr><td>Логин</td><td>{{ adminStore.profile.username }}</td></tr>
          <tr><td>E-mail</td><td>{{ adminStore.profile.email }}</td></tr>
          <tr><td>Регион</td><td>{{ storeLocation.regionsObject[adminStore.profile.region_id as string] }}</td></tr>
          <tr><td>Создан</td><td>{{ new Date(adminStore.profile.pswd_create).toLocaleString('ru-RU') }}</td></tr>
          <tr><td>Изменен</td><td>{{ new Date(adminStore.profile.pswd_change).toLocaleString('ru-RU') }}</td></tr>
          <tr><td>Вход</td><td>{{ new Date(adminStore.profile.last_login).toLocaleString('ru-RU')}}</td></tr>
          <tr><td>Роль</td><td>{{ adminStore.profile.role }}</td></tr>
          <tr><td>Попыток входа</td><td>{{ adminStore.profile.attempt }}</td></tr>
          <tr><td>Блокировка</td><td>{{ isBlocked }}</td></tr>
        </tbody>
      </table>
      <div class="btn-group py-2" role="group">
        <button @click="adminStore.editUserInfo('block')" class="btn btn-outline-primary">
          {{adminStore.profile.blocked ? "Разблокировать" : 'Заблокировать' }}
        </button>
        <button @click="adminStore.action = 'edit'" class="btn btn-outline-primary">Редактировать</button>
        <button @click="adminStore.editUserInfo('drop')" class="btn btn-outline-primary">Сбросить пароль</button>
        <button @click="adminStore.editUserInfo('delete')" class="btn btn-outline-primary">Удалить</button>
      </div>
    </div>
  </div>
</template>@/store/admin