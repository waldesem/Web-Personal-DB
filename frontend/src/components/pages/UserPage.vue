<script setup lang="ts">

import { defineAsyncComponent, onBeforeMount } from 'vue';
import { onBeforeRouteLeave, useRoute } from 'vue-router';
import { adminStore } from '@store/admins';
import { classifyStore } from '@/store/classify';
import { clearItem } from '@share/utilities';
//import PhotoCard from '@components/layouts/PhotoCard.vue';

const HeaderDiv = defineAsyncComponent(() => import('@components/layouts/HeaderDiv.vue'));
const UserForm = defineAsyncComponent(() => import('@components/forms/UserForm.vue'));

const storeClassify = classifyStore();
const storeAdmin = adminStore();

const route = useRoute();

storeAdmin.userData.id = route.params.id.toString();

onBeforeMount(async () => {
  storeAdmin.userData.userAction('view');
});

onBeforeRouteLeave((_to: any, _from: any, next: () => void) => {
  clearItem(storeAdmin.userData.form);
  Object.assign(storeAdmin.userData.profile, {
    id: '',
    fullname: '',
    region_id: '',
    username: '',
    email: '',
    pswd_create: '',
    pswd_change: '',
    last_login: '',
    roles: [],
    groups: [],
    blocked: '',
    attempt: ''
  });
  next()
})

</script>

<template>
  <div class="container py-3">
    <HeaderDiv :page-header="'Профиль пользователя'" />
    <div class="py-3">
      <!--PhotoCard :profileId="storeAdmin.profileData.id" :imageUrl="storeAdmin.profileData.image"/-->
      <table class="table table-responsive">
        <thead>
          <tr><th colspan="2"># {{ storeAdmin.userData.id }}</th></tr>
        </thead>
        <tbody>
          <tr>
            <td width="35%">Имя пользователя</td>
            <td>{{storeAdmin.userData.profile.fullname }}</td>
          </tr>
          <tr>
            <td>Логин</td><td>{{ storeAdmin.userData.profile.username }}</td>
          </tr>
          <tr>
            <td>E-mail</td><td>{{ storeAdmin.userData.profile.email }}</td>
          </tr>
          <tr>
            <td>Регион</td>
            <td>{{ storeClassify.classifyItems.regions[storeAdmin.userData.profile.region_id] }}</td>
          </tr>
          <tr>
            <td>Создан</td>
            <td>{{ new Date(storeAdmin.userData.profile.pswd_create).toLocaleString('ru-RU') }}</td>
          </tr>
          <tr>
            <td>Изменен</td>
            <td>{{ new Date(storeAdmin.userData.profile.pswd_change).toLocaleString('ru-RU') }}</td>
          </tr>
          <tr>
            <td>Вход</td>
            <td>{{ new Date(storeAdmin.userData.profile.last_login).toLocaleString('ru-RU')}}</td>
          </tr>
          <tr><td>Группы</td>
            <td>
              <ul v-for="(group, index) in storeAdmin.userData.profile.groups" :key=index>
                <li>{{ storeClassify.classifyItems.groups[group['group']] }}
                  <a href="#" @click="storeAdmin.userData.updateGroupRole('delete', 'group', group['group'])">
                    <i class="bi bi-dash-circle"></i>
                  </a>
                </li>
              </ul>
              <form class="form form-check" role="form">
                <select class="form-select" id="group" name="group" 
                        v-model="storeAdmin.userData.group" 
                        @change="storeAdmin.userData.updateGroupRole('add', 'group', storeAdmin.userData.group)">
                  <option value="" selected>Добавить группу</option>
                  <option v-for="(val, name) in storeClassify.classifyItems.groups" 
                          :key="name" :value="name">
                    {{ val }}</option>
                </select>
              </form>
            </td>
          </tr>
          <tr><td>Роли</td>
            <td>
              <ul v-for="(role, index) in storeAdmin.userData.profile.roles" :key=index>
                <li>{{ role['role'] }}
                  <a href="#" @click="storeAdmin.userData.updateGroupRole('delete', 'role',role['role'])">
                    <i class="bi bi-dash-circle"></i>
                  </a>
                </li>
              </ul>
              <form class="form form-check" role="form">
                <select class="form-select" id="role" name="role" 
                    v-model="storeAdmin.userData.role" 
                    @change="storeAdmin.userData.updateGroupRole('add', 'role', storeAdmin.userData.role)">
                  <option value="" selected>Добавить роль</option>
                  <option v-for="(val, name) in storeClassify.classifyItems.roles" 
                          :key="name" :value="val">
                    {{ val }}</option>
                </select>
              </form>
            </td>
          </tr>
          <tr>
            <td>Попыток входа</td>
            <td>{{ storeAdmin.userData.profile.attempt }}</td>
          </tr>
          <tr>
            <td>Блокировка</td>
            <td>{{ storeAdmin.userData.profile.blocked ? 'Заблокирован' : 'Разблокирован' }}</td>
          </tr>
        </tbody>
      </table>
      <div class="btn-group py-3" role="group">
        <button class="btn btn-outline-primary" type="button" 
                data-bs-toggle="modal" data-bs-target="#modalUser"
                @click="storeAdmin.userData.action = 'edit';
                storeAdmin.userData.form = storeAdmin.userData.profile">
          Изменить пользователя
        </button>
        <button @click="storeAdmin.userData.userAction('block')" class="btn btn-outline-primary">
          {{storeAdmin.userData.profile.blocked ? "Разблокировать" : 'Заблокировать' }}
        </button>
        <button @click="storeAdmin.userData.userAction('drop')" type="button" class="btn btn-outline-primary">
          Сбросить пароль
        </button>
        <button @click="storeAdmin.userData.userDelete" type="button" class="btn btn-outline-primary">
          Удалить
        </button>
      </div>
    </div>
    <UserForm />
  </div>
</template>

<style scoped>

ul, li {
padding: 0;
list-style: none;
}
</style>