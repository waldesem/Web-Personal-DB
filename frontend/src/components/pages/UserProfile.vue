<script setup lang="ts">
// Компонент страницы профиля пользователя

import { onBeforeMount, ref } from 'vue'
import { useRoute } from 'vue-router';
import { appAuth } from '@store/auth';
import { locationStore } from '@store/location';
import router from '@router/router';
import server from '@store/server';
import UserForm from '@content/UserForm.vue'

// Объявление событиия отправки сообщения
const emit = defineEmits(['updateMessage']);

const storeAuth = appAuth()

const storeLocation = locationStore();

const route = useRoute();

const action = ref('');  // Выбор действия

const userId = route.params.id;  // ID пользователя из роута 

// Данные пользователя
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

// Инициализация данных пользователя
onBeforeMount(async () => {
  viewUser(userId as String);
});

/**
 * Fetches user data from the server based on the provided ID and updates the profile value.
 *
 * @param {String} id - The ID of the user to fetch data for.
 * @return {Promise<void>} - A promise that resolves when the user data is fetched and the profile value is updated.
 */
async function viewUser(id: String): Promise<void>{
  try {
    const response = await storeAuth.axiosInstance.get(`${server}/user/${id}`);
    const datas = response.data;
    profile.value = datas;
    
  } catch (error) {
    console.error(error);
  }
};


/**
 * Edits user information based on the given flag.
 *
 * @param {String} flag - The flag indicating the type of edit to perform.
 * @return {Promise<void>} - A promise that resolves when the user information has been edited.
 */
async function editUserInfo(flag: String): Promise<void> {
  // Матчинг заголовка окна подтверждения действия
  const confirm_title = {
    'delete': 'окончательно удалить',
    'block': 'блокировать/разблокировать',
    'drop': 'сбросить пароль'
  };
  if (confirm(`Вы действительно хотите ${confirm_title[flag as keyof typeof confirm_title]} пользователя?`)) {

    try {
      const response = await storeAuth.axiosInstance.get(`${server}/user/${userId}/${flag}`);
      const { user } = response.data;
      
      // Матчинг атрибута и текста сообщения
      const resp = {
        'True': ['alert-success', 'Пользователь заблокирован'],
        'False': ['alert-success', 'Пользователь разблокирован'],
        'delete': ['alert-danger', 'Пользователь удалён'],
        'drop': ['alert-success', 'Пароль пользователя удален'],
        'None': ['alert-danger', 'Возникла ошибка'],
      };
      // Обновление сообщения
      emit('updateMessage',{
        attr: resp[user as keyof typeof resp][0],
        text: resp[user as keyof typeof resp][1]
      });
      // Обновление страницы либо редирект на страницу списка пользователей
      user !== 'delete' ? viewUser(userId as String) : router.push({ name: 'users' })
    
    } catch (error) {
      console.error(error);
    }
  }
}

</script>


<template>
  <div class="container py-3">
    <div class="py-5"><h4>Профиль пользователя</h4></div>
    <UserForm v-if="action === 'edit'" 
              :action="action" 
              :profile="profile" 
              @updateMessage="emit('updateMessage')" 
              @updateAction="action = ''"/>
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
        <button @click="action = 'edit'" class="btn btn-outline-primary">Редактировать</button>
        <button @click="editUserInfo('drop')" class="btn btn-outline-primary">Сбросить пароль</button>
        <button @click="editUserInfo('delete')" class="btn btn-outline-primary">Удалить</button>
      </div>
    </div>
  </div>
</template>