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

adminStore.userData.userId = route.params.id as string;

onBeforeMount(async () => {
  adminStore.userAction('view');
});

const isBlocked = computed(() => {
  return adminStore.profileData.blocked ? 'Заблокирован' : 'Разблокирован';
});

</script>

<template>
  <div class="container py-3">
    <div class="py-3"><h4>Профиль пользователя</h4></div>
    <UserForm v-if="adminStore.userData.userAct === 'edit'" />
    <div v-else class="py-2">
      <table class="table table-responsive">
        <thead>
          <tr><th colspan="2"># {{ adminStore.profileData.id }}</th></tr>
        </thead>
        <tbody>
          <tr>
            <td width="35%">Имя пользователя</td>
            <td>{{adminStore.profileData.fullname }}</td>
          </tr>
          <tr>
            <td>Логин</td>
            <td>{{ adminStore.profileData.username }}</td>
          </tr>
          <tr>
            <td>E-mail</td>
            <td>{{ adminStore.profileData.email }}</td>
          </tr>
          <tr>
            <td>Регион</td>
            <td>{{ storeClassify.regions[adminStore.profileData.region_id] }}</td>
          </tr>
          <tr>
            <td>Создан</td>
            <td>{{ new Date(adminStore.profileData.pswd_create).toLocaleString('ru-RU') }}</td>
          </tr>
          <tr>
            <td>Изменен</td>
            <td>{{ new Date(adminStore.profileData.pswd_change).toLocaleString('ru-RU') }}</td>
          </tr>
          <tr>
            <td>Вход</td>
            <td>{{ new Date(adminStore.profileData.last_login).toLocaleString('ru-RU')}}</td>
          </tr>
          <tr><td>Группы</td>
            <td>
              <ul v-for="(group, index) in adminStore.profileData.groups" :key=index>
                <li>{{ storeClassify.groups[group['group']] }}
                  <a href="#" @click="adminStore.delRoleGroup('group', group['group'])">
                    <i class="bi bi-dash-circle"></i>
                  </a>
                </li>
              </ul>
              <form class="form form-check" role="form">
                <select class="form-select" id="group" name="group" 
                    v-model="adminStore.userData.userGroup" 
                    @change="adminStore.addGroupRole('group', adminStore.userData.userGroup)">
                  <option value="" selected>Добавить группу</option>
                  <option v-for="(val, name) in storeClassify.groups" :key="name" :value="name">
                    {{ val }}</option>
                </select>
              </form>
            </td>
          </tr>
          <tr><td>Роли</td>
            <td>
              <ul v-for="(role, index) in adminStore.profileData.roles" :key=index>
                <li>{{ role['role'] }}
                  <a href="#" @click="adminStore.delRoleGroup('role',role['role'])">
                    <i class="bi bi-dash-circle"></i>
                  </a>
                </li>
              </ul>
              <form class="form form-check" role="form">
                <select class="form-select" id="role" name="role" 
                    v-model="adminStore.userData.userRole" 
                    @change="adminStore.addGroupRole('role', adminStore.userData.userRole)">
                  <option value="" selected>Добавить роль</option>
                  <option v-for="(val, name) in storeClassify.roles" :key="name" :value="val">
                    {{ val }}</option>
                </select>
              </form>
            </td>
          </tr>
          <tr><td>Попыток входа</td><td>{{ adminStore.profileData.attempt }}</td></tr>
          <tr><td>Блокировка</td><td>{{ isBlocked }}</td></tr>
        </tbody>
      </table>
      <div class="btn-group py-3" role="group">
        <button @click="adminStore.userAction('block')" class="btn btn-outline-primary">
          {{adminStore.profileData.blocked ? "Разблокировать" : 'Заблокировать' }}
        </button>
        <button @click="adminStore.userData.userAct = 'edit'" class="btn btn-outline-primary">
            Редактировать</button>
        <button @click="adminStore.userAction('drop')" class="btn btn-outline-primary">
            Сбросить пароль</button>
        <button @click="adminStore.userDelete" class="btn btn-outline-primary">
            Удалить</button>
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