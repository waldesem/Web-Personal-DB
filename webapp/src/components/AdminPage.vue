<script setup lang="ts">

import { ref, computed, onBeforeMount } from 'vue'
import axios from 'axios';
import config from '@/config';
import AlertMessage from './AlertMessage.vue';
import router from '@/router';


const data = ref({
  actions: 'create',
  logs: [],
  users: [],
  regions: [],
  profile: {
    id: '',
    fullname: '',
    region_id: 0,
    username: '',
    pswd_create: '',
    pswd_change: '',
    last_login: '',
    blocked: '',
    role: '',
  },
  user_id: '',
  attr: '',
  text: ''
});

const headers  = {
  headers: {'Authorization': `Bearer ${localStorage.getItem('access_token')}`}
};


onBeforeMount(async () => {
  const response = await axios.get(`${config.appUrl}/admin/admin`, headers);
  const { admin } = response.data;
  if (!admin) {
    router.push({ name: 'login' })
  } else {
    try {
        Promise.all([
        getUsers(),
        logAction('new'),
        regionList()
      ])
    } catch (error) {
      console.error(error)
      router.push({ name: 'login' })
    }
  }
});


async function getUsers(){
  try {
    const response = await axios.get(`${config.appUrl}/admin/index`, headers);
    data.value.users = response.data;
  } catch (error) {
    console.error(error);
  }
};

async function submitData(flag: String){
  try {  
    const response = await axios.post(`${config.appUrl}/user/update/${flag}/${data.value.user_id}`, {
      'fullname': data.value.profile['fullname'], 
      'username': data.value.profile['username'],
      'region_id': data.value.profile['region_id'],
      'role': data.value.profile['role']
      }, headers);
    const  { user } = response.data;
    const resp = {
      'create': ['alert-success', 'Пользователь успешно создан'],
      'edit': ['alert-success', 'Пользователь успешно изменен'],
      'none': ['alert-danger', 'Ошибка создания (пользователь существует)/редактирования']
    }
    data.value.attr = resp[user as keyof typeof resp][0];
    data.value.text = resp[user as keyof typeof resp][1];
    data.value.actions = user === 'none' ? 'create' : 'create';
    getUsers();
  } catch (error) {
    console.error(error);
  }
};


async function viewUser(id: String){
  data.value.actions = 'profile';
  try {
    const response = await axios.get(`${config.appUrl}/user/profile/${id}`, headers);
    const datas = response.data;
    data.value.profile = datas;
    data.value.user_id = datas['id']
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
      const response = await axios.get(`${config.appUrl}/user/action/${flag}/${data.value.user_id}`, headers);
      const { user } = response.data;
      const resp = {
        'True': ['alert-success', 'Пользователь заблокирован'],
        'False': ['alert-success', 'Пользователь разблокирован'],
        'delete': ['alert-danger', 'Пользователь удалён'],
        'drop': ['alert-success', 'Пароль пользователя удален'],
        'None': ['alert-danger', 'Возникла ошибка'],
      }
      data.value.attr = resp[user as keyof typeof resp][0];
      data.value.text = resp[user as keyof typeof resp][1];
      data.value.actions = user !== 'delete' ? 'profile' : 'create';
      user !== 'delete' ? viewUser(data.value.user_id) : getUsers()
    } catch (error) {
      console.error(error);
    }
  }
}


async function regionList(){
  const response = await axios.get(`${config.appUrl}/region/list`);
  const locations  = response.data;
  data.value.regions = locations.reduce(
  (acc: {[key: number]: string}, obj: {id: number, region: string}) => {
  acc[obj.id] = obj.region;
  return acc;
  }, {}
);
};
  

async function addRegion() {
  const response = await axios.post(`${config.appUrl}/region/add`, {
    'region': data.value.profile['region_id']
    }, headers);
  const  { location } = response.data;
  data.value.attr = location ? 'alert-warning' : 'alert-success' ;
  data.value.text = location 
    ? 'При добавлении записи возникла ошибка'
    : 'Запись добавлена. Для применения изменений необходим перезапуск сервера';
  regionList();
};

async function delRegion(id: String) {
  if (confirm(`Вы действительно хотите удалить регион?`)) {
    const response = await axios.get(`${config.appUrl}/region/delete/${id}`, headers);
    const  { location } = response.data;
    data.value.attr = 'alert-success';
    data.value.text = `Регион ${location} удален. Перезапустите приложение`;
    regionList()
  }
};

async function logAction(flag: string) {
  try {
    const response = await axios.get(`${config.appUrl}/logs/${flag}`, headers);
    data.value.logs = response.data;
  } catch (error) {
    console.error(error);
  }
}

const header = computed(() => {
  const actionHeader = {
  'create': 'Список пользователей',
  'region': 'Список регионов',
  'profile': 'Профиль пользователя',
  'logs': "Системные сообщения"
  }
  return actionHeader[data.value.actions as keyof typeof actionHeader]
});

const count = computed(() => {
  return data.value.logs ? data.value.logs.length : 0
});

</script>


<template>
  <div class="container-fluid">
    <nav class="navbar navbar-expand navbar-nav mr-auto navbar-dark bg-secondary">
      <div class="container">
        <a class="nav-link active">Admin-StaffSec</a>
        <div class="navbar-nav mr-auto collapse navbar-collapse" id="navbarContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <a @click="getUsers(); data.actions = 'create'" class="nav-link active" href="#">Пользователи</a>
            </li>
            <li class="nav-item">
              <a @click="regionList(); data.actions = 'region'" class="nav-link active" href="#" >Регионы</a>
            </li>
            <li class="nav-item">
              <a @click="logAction('new'); data.actions = 'logs'" class="nav-link active" href="#">Сообщения
                <span class="position-absolute translate-middle badge rounded-pill text-bg-success">{{count}}</span>
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
    
    <!--Create new user profile-->
    <div v-if="data.actions === 'create' || data.actions === 'edit'" class="py-3">
      <form @submit.prevent="submitData(data.actions)" class="form form-check" role="form">
        <div class="row mb-3">
          <div class="col-md-6">
            <div class="row">
              <label class="col-form-label col-lg-4" for="fullname">Имя пользователя:</label>
              <div class="col-lg-8">
                <input autocomplete="fullname" class="form-control" minlength="3" maxlength="25" name="fullname" 
                  placeholder="Имя пользователя" required type="text" v-model="data.profile['fullname']" pattern="[a-zA-Z ]+">
              </div>
            </div>
          </div>
          <div class="col-md-5">
            <div class="row">
              <label class="col-form-label col-lg-4" for="username">Учетная запись:</label>
              <div class="col-lg-8">
                <input :disabled="data.actions === 'edit'" autocomplete="username" class="form-control" minlength="3" maxlength="25" name="username" 
                  placeholder="Логин без пробелов на латинице" required type="text" v-model="data.profile['username']" pattern="[a-zA-Z]+">
              </div>
            </div>
          </div>
        </div>
        <div class="row mb-3">
          <div class="col-md-6">
            <div class="row">
              <label class="col-form-label col-lg-4" for="role">Роль:</label>
              <div class="col-lg-8">
                <select class="form-select" id="role" name="role" v-model="data.profile['role']" required>
                  <option v-for="(value, name) in config.roles" :value=value :key="name">{{name}}</option>                
                </select>
              </div>
            </div>
          </div>
          <div class="col-md-5">
            <div class="row">
              <label class="col-form-label col-lg-4" for="region">Регион:</label>
              <div class="col-lg-8">
                <select class="form-select" id="region" name="region" v-model="data.profile['region_id']" required>
                  <option v-for="name, value in data.regions" :value="value">{{name}}</option>                
                </select>
              </div>
            </div>
          </div>
          <div class="col-md-1">
            <button class="btn btn-outline-primary" name="submit" type="submit">{{data.actions === 'create' ? 'Создать' : 'Изменить'}}</button>
          </div>
        </div>
      </form>
    </div>
    
    <!--Users table-->
    <div v-if="data.actions === 'create'" class="py-3">
      <table class="table table-hover table-responsive align-middle">
        <thead>
          <tr height="50px">
            <th width="5%">#</th>
            <th>Имя пользователя</th>
            <th width="15%">Логин</th>
            <th width="20%">Создан</th>
            <th width="20%">Вход</th>
            <th width="10%">Роль</th>
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
    
    <!--Open user profile-->
    <div v-if="data.actions === 'profile' || data.actions === 'edit'">
      <table class="table table-responsive" >
        <thead>
          <tr><th colspan="2"># {{ data.profile['id'] as any }}</th></tr>
        </thead>
        <tbody>
          <tr><td width="35%">Имя пользователя</td><td>{{data.profile['fullname'] }}</td></tr>
          <tr><td>Логин</td><td>{{ data.profile['username'] }}</td></tr>
          <tr><td>Регион</td><td>{{ data.regions[data.profile['region_id']] }}</td></tr>
          <tr><td>Создан</td><td>{{ new Date(data.profile['pswd_create']).toLocaleString('ru-RU') }}</td></tr>
          <tr><td>Изменен</td><td>{{ new Date(data.profile['pswd_change']).toLocaleString('ru-RU') }}</td></tr>
          <tr><td>Вход</td><td>{{ new Date(data.profile['last_login']).toLocaleString('ru-RU')}}</td></tr>
          <tr><td>Блокировка</td><td>{{data.profile['blocked'] }}</td></tr>
          <tr><td>Роль</td><td>{{ data.profile['role'] }}</td></tr>
        </tbody>
      </table>
      <div class="btn-group py-2" role="group">
        <button @click="editUserInfo('block')" class="btn btn-outline-primary">{{data.profile['blocked'] ? "Разблокировать" : 'Заблокировать' }}</button>
        <button @click="data.actions = 'edit'" class="btn btn-outline-primary">Редактировать</button>
        <button @click="editUserInfo('drop')" class="btn btn-outline-primary">Сбросить пароль</button>
        <button @click="editUserInfo('delete')" class="btn btn-outline-primary">Удалить</button>
      </div>
    </div>
    
    <!--Regions table-->
    <div v-if="data.actions === 'region'" class="py-3">
      <form @submit.prevent="addRegion" class="form form-check" role="form"> 
        <div class="row mb-3">
          <div class="row">
            <label class="col-form-label col-lg-1" for="region">Регион: </label>
            <div class="col-lg-9">
                <input autocomplete="region" class="form-control" minlength="3" maxlength="25" name="region" 
                      placeholder="Регион" required type="text" v-model="data.profile.region_id">
            </div>
            <div class="col-lg-2">
                <button class="btn btn-outline-primary" name="submit" type="submit">Добавить регион</button>
            </div>
          </div>
        </div>
      
      </form>

      <div class="py-3">
        <table class="table table-hover table-responsive align-middle">
          <thead>
            <tr height="50px">
              <th width="15%">#</th>
              <th>Регион</th>
              <th width="25%">Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr height="50px" v-for="name, value in data.regions">
              <td>{{ value }}</td>
              <td>{{ name }}</td>
              <td><a class="link-opacity-50" href="#" @click="delRegion(value.toString())">Удалить</a></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!--Logs table-->
    <div v-if="data.actions === 'logs'" class="py-3">
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
          <tr v-for="log in data.logs" :key="log">
            <td>{{ log["id" as keyof typeof log] }}</td>
            <td>{{ new Date(log["timestamp" as keyof typeof log]).toLocaleString('ru-RU') }}</td>
            <td>{{ log["level" as keyof typeof log] }}</td>
            <td>{{ log["message" as keyof typeof log] }}</td>
            <td>{{ log["pathname" as keyof typeof log] }}</td>
            <td>{{ log["lineno" as keyof typeof log] }}</td>
          </tr>
        </tbody>
      </table>
      <div class="btn-group py-3" role="group">
        <button @click="logAction('reply')" class="btn btn-outline-primary" type="button">Отметить прочитанными</button>
        <button @click="logAction('delete')" class="btn btn-outline-primary" type="button">Удалить всё</button>
      </div>  
    </div>
  </div>

</template>