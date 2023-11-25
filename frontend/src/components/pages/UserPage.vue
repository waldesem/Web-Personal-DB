<script setup lang="ts">

import { defineAsyncComponent, onBeforeMount } from 'vue';
import { onBeforeRouteLeave, useRoute } from 'vue-router';
import { classifyStore } from '@/store/classify';
import { adminStore } from '@store/admins';
import { clearItem } from '@utilities/utils';

const HeaderDiv = defineAsyncComponent(() => import('@components/layouts/HeaderDiv.vue'));
const RowDivSlot = defineAsyncComponent(() => import('@components/elements/RowDivSlot.vue'));
const UserForm = defineAsyncComponent(() => import('@components/forms/UserForm.vue'));
//const PhotoCard = defineAsyncComponent(() => import('@components/layouts/PhotoCard.vue'));

const storeClassify = classifyStore();
const storeAdmin = adminStore();

const route = useRoute();

storeAdmin.dataUsers.id = route.params.id.toString();

onBeforeMount(async () => {
  storeAdmin.dataUsers.userAction('view');
});

onBeforeRouteLeave((_to: any, _from: any, next: () => void) => {
  clearItem(storeAdmin.dataUsers.form);
  Object.assign(storeAdmin.dataUsers.profile, {
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
}); 

</script>


<template>
  <div class="container py-3">
    <HeaderDiv :page-header="'Профиль пользователя'" />
    <div class="py-3">
      <!--PhotoCard :profileId="storeAdmin.profileData.id" :imageUrl="storeAdmin.profileData.image"/-->
      <div class="d-flex justify-content-start">
        <RowDivSlot :label="'ID'" 
                    :value="storeAdmin.dataUsers.profile.id"/>
        <RowDivSlot :label="'Имя пользователя'" 
                    :value="storeAdmin.dataUsers.profile.fullname"/>
        <RowDivSlot :label="'Логин'" 
                    :value="storeAdmin.dataUsers.profile.username"/>
        <RowDivSlot :label="'E-mail'" 
                    :value="storeAdmin.dataUsers.profile.email"/>
        <RowDivSlot :label="'Регион'" 
                    :value="storeClassify.classData.regions[storeAdmin.dataUsers.profile.region_id]"/>
        <RowDivSlot :label="'Создан'" 
                    :value="new Date(storeAdmin.dataUsers.profile.pswd_create).toLocaleString('ru-RU')"/>
        <RowDivSlot :label="'Изменен'" 
                    :value="new Date(storeAdmin.dataUsers.profile.pswd_change).toLocaleString('ru-RU')"/>
        <RowDivSlot :label="'Вход'" 
                    :value="new Date(storeAdmin.dataUsers.profile.last_login).toLocaleString('ru-RU')"/>
        <RowDivSlot :label="'Попыток входа'" 
                    :value="storeAdmin.dataUsers.profile.attempt"/>
        <RowDivSlot :label="'Блокировка'" 
                    :value="storeAdmin.dataUsers.profile.blocked ? 'Заблокирован' : 'Разблокирован'"/>
        <RowDivSlot :label="'Группы'" :slotTwo="true">
          <template v-slot:divTwo>
            <ul v-for="(group, index) in storeAdmin.dataUsers.profile.groups" :key=index>
              <li>{{ storeClassify.classData.groups[group['group']] }}
                <a href="#" @click="storeAdmin.dataUsers.updateGroupRole('delete', 'group', group['group'])">
                  <i class="bi bi-dash-circle"></i>
                </a>
              </li>
            </ul>
            <form class="form form-check" role="form">
              <select class="form-select" id="group" name="group" 
                      v-model="storeAdmin.dataUsers.group" 
                      @change="storeAdmin.dataUsers.updateGroupRole('add', 'group', storeAdmin.dataUsers.group)">
                <option value="" selected>
                  Добавить группу
                </option>
                <option v-for="(val, name) in storeClassify.classData.groups" :key="name" :value="name">
                  {{ val }}
                </option>
              </select>
            </form>
          </template>
        </RowDivSlot>
        <RowDivSlot :label="'Роли'" :slotTwo="true">
          <template v-slot:divTwo>
            <ul v-for="(role, index) in storeAdmin.dataUsers.profile.roles" :key=index>
              <li>{{ storeClassify.classData.roles[role['role']] }}
                <a href="#" @click="storeAdmin.dataUsers.updateGroupRole('delete', 'role',role['role'])">
                  <i class="bi bi-dash-circle"></i>
                </a>
              </li>
            </ul>
            <form class="form form-check" role="form">
              <select class="form-select" id="role" name="role" 
                  v-model="storeAdmin.dataUsers.role" 
                  @change="storeAdmin.dataUsers.updateGroupRole('add', 'role', storeAdmin.dataUsers.role)">
                <option value="" selected>
                  Добавить роль
                </option>
                <option v-for="(val, name) in storeClassify.classData.roles" :key="name" :value="val">
                  {{ val }}</option>
              </select>
            </form>
          </template>
        </RowDivSlot>
      </div>
      <div class="btn-group py-3" role="group">
        <button class="btn btn-outline-primary" type="button" 
                data-bs-toggle="modal" data-bs-target="#modalUser"
                @click="storeAdmin.dataUsers.action = 'edit';
                storeAdmin.dataUsers.form = storeAdmin.dataUsers.profile">
          Изменить пользователя
        </button>
        <button @click="storeAdmin.dataUsers.userAction('block')" class="btn btn-outline-primary">
          {{storeAdmin.dataUsers.profile.blocked ? "Разблокировать" : 'Заблокировать' }}
        </button>
        <button @click="storeAdmin.dataUsers.userAction('drop')" type="button" class="btn btn-outline-primary">
          Сбросить пароль
        </button>
        <button @click="storeAdmin.dataUsers.userDelete" type="button" class="btn btn-outline-primary">
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