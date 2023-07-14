<template>
  <div class="container-fluid">
    <nav class="navbar navbar-expand navbar-nav mr-auto navbar-dark bg-secondary">
      <div class="container">
        <a class="nav-link active">Admin-StaffSec</a>
        <div class="navbar-nav mr-auto collapse navbar-collapse" id="navbarContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <a @click="getUsers" class="nav-link active" href="#" >Пользователи</a>
            </li>
            <li class="nav-item">
              <a @click="data.actions='create'" class="nav-link active" href="#" >Создать</a>
            </li>
            <li class="nav-item">
              <a @click="data.actions='logs'" class="nav-link active" href="#">Уведомления
                <span class="position-absolute translate-middle badge rounded-pill text-bg-success">{{data.count}}</span>
              </a>
            </li>
          </ul>                                
        </div>
        <div class="d-flex px-2">
          <router-link :to="{name: 'login'}" class="nav-link active" data-bs-toggle="tooltip" data-bs-placement="right" title="Выход"><i class="bi bi-box-arrow-in-right"></i></router-link>
        </div>
      </div>
    </nav>
  </div>

  <div class="container py-5">
    <AlertMessage v-if="data.attr" :attr="data.attr" :text="data.text" />
    <div class="py-5"><h4>{{ header }}</h4></div>
    <!--Users table-->
    <div v-if="data.actions === 'users'">
      <table class="table table-hover table-responsive align-middle">
        <thead>
          <tr height="50px">
            <th width="5%">#</th>
            <th>Имя пользователя</th>
            <th width="20%">Логин</th>
            <th width="15%">Создан</th>
            <th width="15%">Вход</th>
            <th width="20%">Роль</th>
          </tr>
        </thead>
        <tbody>
          <tr height="50px" v-for="user in data.users" :key="user">
            <td>{{ user["id" as keyof typeof user] }}</td>
            <td>{{ user["fullname" as keyof typeof user] }}</td>
            <td><a href="#" @click="viewUser(user['id' as keyof typeof user])">{{ user["username" as keyof typeof user] }}</a></td>
            <td>{{ new Date(user["pswd_create" as keyof typeof user]).toLocaleString('ru-RU') }}</td>
            <td>{{ new Date(user["last_login" as keyof typeof user]).toLocaleString('ru-RU') }}</td>
            <td>{{ user["role" as keyof typeof user] }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <!--Create new user profile-->
    <div v-if="data.actions === 'create'">
      <form @submit.prevent="submitData" class="form form-check" role="form">
          <div class="mb-3 row required">
              <label class="col-form-label col-lg-2" for="fullname">Имя пользователя: </label>
              <div class="col-lg-4">
                  <input autocomplete="fullname" class="form-control" minlength="3" maxlength="25" name="fullname" placeholder="Имя пользователя" required type="text" v-model="data.fullname" pattern="[a-zA-Z]+">
              </div>
          </div>
          <div class="mb-3 row required">
              <label class="col-form-label col-lg-2" for="username">Учетная запись: </label>
                  <div class="col-lg-4">
                      <input autocomplete="username" class="form-control" minlength="3" maxlength="25" name="username" placeholder="Учетная запись без пробелов на латинице" required type="text" v-model="data.username" pattern="[a-zA-Z]+">
                  </div>
              </div>
          <div class="mb-3 row required">
            <label class="col-form-label col-lg-2" for="role">Роль: </label>
              <div class="col-lg-4">
                <select v-for="(value, name) in config.roles" class="form-select" id="role" name="role" v-model="data.role" required>
                  <option value={{value}}>{{name}}</option>                
                </select>
              </div>
          </div>
          <div class=" row">
              <div class="offset-lg-2 col-lg-4">
                <div class="btn-group" role="group">
                  <button class="btn btn-outline-primary" name="submit" type="submit">Создать</button>
                  <button @click="data.actions='users'" class="btn btn-outline-primary" type="button">Отмена</button>
              </div>
              </div>
          </div>
      </form>
    </div>
    <!--Open user profile-->
    <div v-if="data.actions === 'profile'">
      <div v-html="data.profile ? data.profile : ''"></div>      
      <button @click="blockUser" class="btn btn-outline-primary">{{data.blocked ? "Разблокировать" : 'Заблокировать' }}</button>
    </div>
    <!--Logs table-->
    <div v-if="data.actions === 'logs'">
      <table class="table table-hover table-responsive align-middle">
        <thead>
          <tr height="50px">
            <th width="5%">#</th>
            <th width="15%">Время</th>
            <th width="15%">Уровень</th>
            <th >Сообщение</th>
            <th width="15%">Путь</th>
            <th width="15%">Строка</th>
          </tr>
        </thead>
        <tbody>
          <tr height="50px" v-for="log in data.logs" :key="log">
            <td>{{ log["id" as keyof typeof log] }}</td>
            <td>{{ new Date(log["timestamp" as keyof typeof log]).toLocaleString('ru-RU') }}</td>
            <td>{{ log["level" as keyof typeof log] }}</td>
            <td>{{ log["message" as keyof typeof log] }}</td>
            <td>{{ log["pathname" as keyof typeof log] }}</td>
            <td>{{ log["lineno" as keyof typeof log] }}</td>
          </tr>
        </tbody>
      </table>
      <button @click="openLog('read')" class="btn btn-outline-primary" type="button">Отметить прочитанными</button>
    </div>
  </div>

</template>

<script setup lang="ts">

import { ref, computed, onBeforeMount } from 'vue'
import axios from 'axios';
import config from '@/config';
import AlertMessage from './AlertMessage'

const user_labels = [
  '#', 'Имя пользователя', 'Логин', 'Хэш пароля', 'Создан', 'Изменен', 'Вход', 'Блокировка', 'Роль'
];

const data = ref({
  actions: '',
  logs: [],
  users: [],
  profile: '',
  user_id: '',
  blocked: '',
  attr: '',
  text: ''
});

const userForm = ref({
  fullname: '',
  username: '',
  role: ''
})

async function getUsers(){
  try {
    const response = await axios.get(`${config.appUrl}/admin/index`, {
      headers: {'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`}
    });
    const datas = response.data;
    Object.assign(data.value, {
      users: datas,
      actions: 'users',
      attr: '',
      text: ''
    })
  } catch (error) {
    console.error(error);
  }
};

async function submitData(event: Event){
  try {  
    const response = await axios.post(`${config.appUrl}/user/registration`, data.value.userForm, {
      headers: {'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`}
    });
    const  { user } = response.data;
    Object.assign(data.value, {
      actions: user ? 'create' : 'users',
      attr: user ? 'alert-danger' : 'alert-success',
      text: user ? 'Пользователь уже существует' : 'Пользователь успешно создан'
    });
    getUsers()
  } catch (error) {
    console.error(error);
  }
};

async function viewUser(id: string){
  try {
    const response = await axios.get(`${config.appUrl}/user/${id}`, {
      headers: {'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`}
    });
    const datas = response.data;
    Object.assign(data.value, {
      profile: createItemTable(user_labels, datas),
      actions: 'profile',
      user_id: datas['id'],
      blocked: datas['blocked'],
      attr: '',
      text: ''
    })
  } catch (error) {
    console.error(error);
  }
};

function createItemTable(names: string[], response: Object) {
  const rows = names.map((name, i) => {
    if (['pswd_create', 'pswd_change', 'last_login'].includes(Object.keys(response)[i])) {
      return `<tr><td width="25%">${name}</td><td>${new Date(Object.values(response)[i]).toLocaleString('ru-RU')}</td></tr>`
    } else {
      return `<tr><td width="25%">${name}</td><td>${Object.values(response)[i]}</td></tr>`
    }
  }).join('');
  const body = `<tbody>${rows}</tbody>`;
  return `<table class="table table-responsive">${body}</table>`;
};


async function blockUser() {
  try {
    const response = await axios.get(`${config.appUrl}/user/block/${data.value.user_id}`, {
      headers: {'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`}
    });
    const { blocked } = response.data;
    Object.assign(data.value, {
      attr: 'alert-success',
      text: blocked ? 'Пользователь заблокирован' : 'Пользователь разблокирован',
      blocked: blocked
    })
    viewUser(data.value.user_id)
  } catch (error) {
    console.error(error);
  }
}

async function openLog(flag: string) {
  try {
    const response = await axios.get(`${config.appUrl}/admin/log/${flag}`, {
      headers: {'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`}
    });
    data.value.logs = response.data;
  } catch (error) {
    console.error(error);
  }
}

const header = computed(() => {
  const actionHeader = {
  'users': 'Список пользователей',
  'create': 'Создать пользователя',
  'profile': 'Профиль пользователя',
  'logs': "Системные сообщения"
  }
  return actionHeader[data.value.actions as keyof typeof actionHeader]
});

const count = computed(() => {
  return data.value.logs ? data.value.logs.length : 0
});

onBeforeMount(async () => {
  getUsers();
  openLog('new')
});

</script>