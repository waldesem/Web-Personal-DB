import { defineStore } from 'pinia';
import { ref } from 'vue'
import { appAuth } from '@store/auth';
import { appAlert } from '@store/alert';
import router from '@router/router';
import server from '@store/server';


const storeAuth = appAuth()

const storeAlert = appAlert();

export const appUsers = defineStore('appUsers',  () => {

  const users = ref([]);

  const userId = ref('');

  const action = ref('');  // Выбор действия

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

  /**
   * Retrieves a list of users from the server.
   *
   * @return {Promise<void>} - A promise that resolves with the list of users retrieved from the server.
   */
  async function getUsers(): Promise<void>{
    try {
      const response = await storeAuth.axiosInstance.get(`${server}/users`);
      users.value = response.data;
    
    } catch (error) {
      console.error(error);
    }
  };

  /**
   * Fetches user data from the server based on the provided ID and updates the profile value.
   *
   * @param {String} id - The ID of the user to fetch data for.
   * @return {Promise<void>} - A promise that resolves when the user data is fetched and the profile value is updated.
   */
  async function viewUser(id: string = userId.value): Promise<void>{
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
      storeAlert.alertAttr = resp[user as keyof typeof resp][0];
      storeAlert.alertText = resp[user as keyof typeof resp][1];
      // Обновление страницы либо редирект на страницу списка пользователей
      user !== 'delete' ? viewUser(userId.value) : router.push({ name: 'users' })
      
      } catch (error) {
      console.error(error);
      }
    }
  };

  /**
   * Submits data to the server.
   *
   * @return {Promise<void>} A promise that resolves when the data is successfully submitted.
   */
  async function submitData(): Promise<void>{
  try {  
    const response = await storeAuth.axiosInstance.post(`${server}/user/${action.value}`, {
      'fullname': profile.value.fullname,
      'username': profile.value.username,
      'email': profile.value.email,
      'region_id': profile.value.region_id,
      'role': profile.value.role
    });
    const  { user } = response.data;
    // Матчинг атрибута и текста сообщения
    const resp = {
      'create': ['alert-success', 'Пользователь успешно создан'],
      'edit': ['alert-success', 'Пользователь успешно изменен'],
      'none': ['alert-danger', 'Ошибка создания (пользователь существует)/редактирования']
    }
    storeAlert.alertAttr = resp[user as keyof typeof resp][0];
    storeAlert.alertText = resp[user as keyof typeof resp][1];
    
    action.value === 'create' ? getUsers() : viewUser(userId.value);
    action.value = '';

  } catch (error) {
      console.error(error);
  }
  };

    return { users, profile, action, userId, getUsers, editUserInfo, submitData, viewUser };
});