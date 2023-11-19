<script setup lang="ts">

import { defineAsyncComponent, onBeforeMount } from 'vue';
import { onBeforeRouteLeave, useRoute } from 'vue-router';
import { adminStore } from '@store/admin';
import { classifyStore } from '@/store/classify';
import { clearItem } from '@share/utilities';
//import PhotoCard from '@components/layouts/PhotoCard.vue';

const HeaderDiv = defineAsyncComponent(() => import('@components/layouts/HeaderDiv.vue'));
const UserForm = defineAsyncComponent(() => import('@components/forms/UserForm.vue'));

const storeClassify = classifyStore();
const storeAdmin = adminStore();

const route = useRoute();

storeAdmin.userData.userId = route.params.id.toString();

onBeforeMount(async () => {
  storeAdmin.userAction('view');
});

onBeforeRouteLeave((_to: any, _from: any, next: () => void) => {
  clearItem(storeAdmin.formData);
  Object.assign(storeAdmin.profileData, {
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
          <tr><th colspan="2"># {{ storeAdmin.profileData.id }}</th></tr>
        </thead>
        <tbody>
          <tr>
            <td width="35%">Имя пользователя</td>
            <td>{{storeAdmin.profileData.fullname }}</td>
          </tr>
          <tr>
            <td>Логин</td><td>{{ storeAdmin.profileData.username }}</td>
          </tr>
          <tr>
            <td>E-mail</td><td>{{ storeAdmin.profileData.email }}</td>
          </tr>
          <tr>
            <td>Регион</td>
            <td>{{ storeClassify.classifyItems.regions[storeAdmin.profileData.region_id] }}</td>
          </tr>
          <tr>
            <td>Создан</td>
            <td>{{ new Date(storeAdmin.profileData.pswd_create).toLocaleString('ru-RU') }}</td>
          </tr>
          <tr>
            <td>Изменен</td>
            <td>{{ new Date(storeAdmin.profileData.pswd_change).toLocaleString('ru-RU') }}</td>
          </tr>
          <tr>
            <td>Вход</td>
            <td>{{ new Date(storeAdmin.profileData.last_login).toLocaleString('ru-RU')}}</td>
          </tr>
          <tr><td>Группы</td>
            <td>
              <ul v-for="(group, index) in storeAdmin.profileData.groups" :key=index>
                <li>{{ storeClassify.classifyItems.groups[group['group']] }}
                  <a href="#" @click="storeAdmin.updateGroupRole('delete', 'group', group['group'])">
                    <i class="bi bi-dash-circle"></i>
                  </a>
                </li>
              </ul>
              <form class="form form-check" role="form">
                <select class="form-select" id="group" name="group" 
                        v-model="storeAdmin.userData.userGroup" 
                        @change="storeAdmin.updateGroupRole('add', 'group', storeAdmin.userData.userGroup)">
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
              <ul v-for="(role, index) in storeAdmin.profileData.roles" :key=index>
                <li>{{ role['role'] }}
                  <a href="#" @click="storeAdmin.updateGroupRole('delete', 'role',role['role'])">
                    <i class="bi bi-dash-circle"></i>
                  </a>
                </li>
              </ul>
              <form class="form form-check" role="form">
                <select class="form-select" id="role" name="role" 
                    v-model="storeAdmin.userData.userRole" 
                    @change="storeAdmin.updateGroupRole('add', 'role', storeAdmin.userData.userRole)">
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
            <td>{{ storeAdmin.profileData.attempt }}</td>
          </tr>
          <tr>
            <td>Блокировка</td>
            <td>{{ storeAdmin.profileData.blocked ? 'Заблокирован' : 'Разблокирован' }}</td>
          </tr>
        </tbody>
      </table>
      <div class="btn-group py-3" role="group">
        <button class="btn btn-outline-primary" type="button" 
                data-bs-toggle="modal" data-bs-target="#modalUser"
                @click="storeAdmin.userData.userAct = 'edit';
                storeAdmin.formData = storeAdmin.profileData">
          Изменить пользователя
        </button>
        <button @click="storeAdmin.userAction('block')" class="btn btn-outline-primary">
          {{storeAdmin.profileData.blocked ? "Разблокировать" : 'Заблокировать' }}
        </button>
        <button @click="storeAdmin.userAction('drop')" type="button" class="btn btn-outline-primary">
          Сбросить пароль
        </button>
        <button @click="storeAdmin.userDelete" type="button" class="btn btn-outline-primary">
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