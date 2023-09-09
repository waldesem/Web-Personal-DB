<script setup lang="ts">
// Компонент страницы профиля пользователя

import { computed, onBeforeMount } from 'vue';
import { appClassify } from '@store/classify';
import { storeAdmin } from '@store/admin';
import { useRoute } from 'vue-router';
import UserForm from '@content/forms/UserForm.vue'

const route = useRoute();
const adminStore = storeAdmin();
const storeClassify = appClassify();

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
          <tr><td>Регион</td><td>{{ storeClassify.regions[adminStore.profile.region_id] }}</td></tr>
          <tr><td>Создан</td><td>{{ new Date(adminStore.profile.pswd_create).toLocaleString('ru-RU') }}</td></tr>
          <tr><td>Изменен</td><td>{{ new Date(adminStore.profile.pswd_change).toLocaleString('ru-RU') }}</td></tr>
          <tr><td>Вход</td><td>{{ new Date(adminStore.profile.last_login).toLocaleString('ru-RU')}}</td></tr>
          <tr><td>Группы</td>
            <td>
              <ul v-for="(group, index) in adminStore.profile.groups" :key=index>
                <li>{{ storeClassify.groups[group['group']] }}
                  <a href="#" @click="adminStore.editGroupRole('group', 'remove', group['group'])">
                    <i class="bi bi-dash-circle"></i>
                  </a>
                </li>
              </ul>
              <form class="form form-check" role="form">
                <select class="form-select" id="group" name="group" 
                    v-model="adminStore.orRoleGroup" @change="adminStore.editGroupRole('group', 'add')">
                  <option value="" selected>Добавить группу</option>
                  <option v-for="(val, name) in storeClassify.groups" :key="name" :value="name">
                    {{ val }}</option>
                </select>
              </form>
            </td>
          </tr>
          <tr><td>Роли</td>
            <td>
              <ul v-for="(role, index) in adminStore.profile.roles" :key=index>
                <li>{{ role['role'] }}
                  <a href="#" @click="adminStore.editGroupRole('role', 'remove', role['role'])">
                    <i class="bi bi-dash-circle"></i>
                  </a>
                </li>
              </ul>
              <form class="form form-check" role="form">
                <select class="form-select" id="role" name="role" 
                    v-model="adminStore.orRoleGroup" @change="adminStore.editGroupRole('role', 'add')">
                  <option value="" selected>Добавить роль</option>
                  <option v-for="(val, name) in storeClassify.roles" :key="name" :value="val">
                    {{ val }}</option>
                </select>
              </form>
            </td>
          </tr>
          <tr><td>Попыток входа</td><td>{{ adminStore.profile.attempt }}</td></tr>
          <tr><td>Блокировка</td><td>{{ isBlocked }}</td></tr>
        </tbody>
      </table>
      <div class="btn-group py-3" role="group">
        <button @click="adminStore.editUserInfo('block')" class="btn btn-outline-primary">
          {{adminStore.profile.blocked ? "Разблокировать" : 'Заблокировать' }}
        </button>
        <button @click="adminStore.action = 'edit'" class="btn btn-outline-primary">Редактировать</button>
        <button @click="adminStore.editUserInfo('drop')" class="btn btn-outline-primary">Сбросить пароль</button>
        <button @click="adminStore.editUserInfo('delete')" class="btn btn-outline-primary">Удалить</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
ul, li {
  padding: 0;
  list-style: none;
}

form {
  padding-left: 0;
  width: 30%;
}
</style>