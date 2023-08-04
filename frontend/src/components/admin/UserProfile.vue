<script setup lang="ts">

import { onBeforeMount, ref } from 'vue'
import { useRoute } from 'vue-router';
import axios from 'axios';
import router from '../../router';
import config from '../../config';
import AlertMessage from '../AlertMessage.vue';
import FooterDiv from '../FooterDiv.vue';
import UserForm from './UserForm.vue'
import NavbarAdmin from './NavbarAdmin.vue';


const route = useRoute();

const data = ref({
  attr: '',
  text: '',
  actions: '',
  regions: [],
  userId: route.params.id
});

const profile = ref({
  id: '',
  fullname: '',
  region_id: 0,
  username: '',
  email: '',
  pswd_create: '',
  pswd_change: '',
  last_login: '',
  role: '',
  blocked: '',
  attempt: ''
});


onBeforeMount(async () => {
  viewUser(data.value.userId as String);
  const response = await axios.get(`${config.appUrl}/locations`);
  const locations  = response.data;
  data.value.regions = locations.reduce(
    (acc: {[key: number]: string}, obj: {id: number, region: string}) => {
    acc[obj.id] = obj.region;
    return acc;
    }, {}
  );
});

async function viewUser(id: String){
    try {
      const response = await axios.get(`${config.appUrl}/admin/user/get/${id}`, {
        headers: {'Authorization': `Bearer ${localStorage.getItem('access_token')}`}
      });
      const datas = response.data;
      profile.value = datas;
      data.value.userId = datas['id']
    } catch (error) {
      console.error(error);
    }
  };

async function editUserInfo(flag: String) {
  const confirm_title = {
    'delete': 'окончательно удалить',
    'block': 'блокировать/разблокировать',
    'drop': 'сбросить пароль'
  };  
  if (confirm(`Вы действительно хотите ${confirm_title[flag as keyof typeof confirm_title]} пользователя?`)) {
    try {
      const response = await axios.get(`${config.appUrl}/admin/user/${data.value.userId}/get/${flag}`, {
        headers: {'Authorization': `Bearer ${localStorage.getItem('access_token')}`}
      });
      const { user } = response.data;
      
      const resp = {
        'True': ['alert-success', 'Пользователь заблокирован'],
        'False': ['alert-success', 'Пользователь разблокирован'],
        'delete': ['alert-danger', 'Пользователь удалён'],
        'drop': ['alert-success', 'Пароль пользователя удален'],
        'None': ['alert-danger', 'Возникла ошибка'],
      };
      data.value.attr = resp[user as keyof typeof resp][0];
      data.value.text = resp[user as keyof typeof resp][1];
      user !== 'delete' ? viewUser(data.value.userId as String) : router.push({ name: 'users' })
    
    } catch (error) {
      console.error(error);
    }
  }
}

</script>


<template>
  <NavbarAdmin />
  <div class="container py-5">
    <AlertMessage v-if="data.attr" :attr="data.attr" :text="data.text" />
    <div class="py-5"><h4>Профиль пользователя</h4></div>
    <UserForm v-if="data.actions" :action="data.actions" :profile="profile" />
    <div v-else class="py-2">
      <table class="table table-responsive" >
        <thead>
          <tr><th colspan="2"># {{ profile.id as any }}</th></tr>
        </thead>
        <tbody>
          <tr><td width="35%">Имя пользователя</td><td>{{profile.fullname }}</td></tr>
          <tr><td>Логин</td><td>{{ profile.username }}</td></tr>
          <tr><td>E-mail</td><td>{{ profile.email }}</td></tr>
          <tr><td>Регион</td><td>{{ data.regions[profile.region_id] }}</td></tr>
          <tr><td>Создан</td><td>{{ new Date(profile.pswd_create).toLocaleString('ru-RU') }}</td></tr>
          <tr><td>Изменен</td><td>{{ new Date(profile.pswd_change).toLocaleString('ru-RU') }}</td></tr>
          <tr><td>Вход</td><td>{{ new Date(profile.last_login).toLocaleString('ru-RU')}}</td></tr>
          <tr><td>Роль</td><td>{{ profile.role }}</td></tr>
          <tr><td>Попыток входа</td><td>{{profile.attempt }}</td></tr>
          <tr><td>Блокировка</td><td>{{profile.blocked }}</td></tr>
        </tbody>
      </table>
      <div class="btn-group py-2" role="group">
        <button @click="editUserInfo('block')" class="btn btn-outline-primary">{{profile.blocked ? "Разблокировать" : 'Заблокировать' }}</button>
        <button @click="data.actions = 'edit'" class="btn btn-outline-primary">Редактировать</button>
        <button @click="editUserInfo('drop')" class="btn btn-outline-primary">Сбросить пароль</button>
        <button @click="editUserInfo('delete')" class="btn btn-outline-primary">Удалить</button>
      </div>
    </div>
  </div>
  <FooterDiv />
</template>../../router/router