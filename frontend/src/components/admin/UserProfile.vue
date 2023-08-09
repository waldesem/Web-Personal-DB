<script setup lang="ts">

import { onBeforeMount, ref } from 'vue'
import { useRoute } from 'vue-router';
import { appAuth } from '../../store/auth';
import { locationStore } from '../../store/location';
import router from '../../router/router';
import server from '../../store/server';
import UserForm from './UserForm.vue'

const emit = defineEmits(['updateMessage']);

const storeAuth = appAuth()

const storeLocation = locationStore();

const route = useRoute();

const data = ref({
  actions: '',
  regions: [],
  userId: route.params.id
});

const profile = ref({
  id: '',
  fullname: '',
  region_id: '',
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
});


function updateMessage(alert: Object) {
  emit('updateMessage', alert)
};


async function viewUser(id: String){
  try {
    const response = await storeAuth.axiosInstance.get(`${server}/user/${id}`);
    const datas = response.data;
    profile.value = datas;
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
      const response = await storeAuth.axiosInstance.get(`${server}/user/${data.value.userId}/${flag}`);
      const { user } = response.data;
      
      const resp = {
        'True': ['alert-success', 'Пользователь заблокирован'],
        'False': ['alert-success', 'Пользователь разблокирован'],
        'delete': ['alert-danger', 'Пользователь удалён'],
        'drop': ['alert-success', 'Пароль пользователя удален'],
        'None': ['alert-danger', 'Возникла ошибка'],
      };

      updateMessage({
        attr: resp[user as keyof typeof resp][0],
        text: resp[user as keyof typeof resp][1]
      });
      user !== 'delete' ? viewUser(data.value.userId as String) : router.push({ name: 'users' })
    
    } catch (error) {
      console.error(error);
    }
  }
}


</script>


<template>
  <div class="container py-3">
    <div class="py-5"><h4>Профиль пользователя</h4></div>
    <UserForm v-if="data.actions === 'edit'" 
              :action="data.actions" 
              :profile="profile" 
              @updateMessage="updateMessage" 
              @updateAction="data.actions = ''"/>
    <div v-else class="py-2">
      <table class="table table-responsive" >
        <thead>
          <tr><th colspan="2"># {{ profile.id }}</th></tr>
        </thead>
        <tbody>
          <tr><td width="35%">Имя пользователя</td><td>{{profile.fullname }}</td></tr>
          <tr><td>Логин</td><td>{{ profile.username }}</td></tr>
          <tr><td>E-mail</td><td>{{ profile.email }}</td></tr>
          <tr><td>Регион</td><td>{{ storeLocation.regionsObject[profile.region_id as string] }}</td></tr>
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
</template>