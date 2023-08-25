import { defineStore } from 'pinia';
import { ref } from 'vue'
import { appAuth } from '@store/auth';
import { appAlert } from '@store/alert';
import { appLocation } from './location';
import router from '@router/router';
import server from '@store/server';


export const storeAdmin = defineStore('storeAdmin',  () => {

  const storeAuth = appAuth();
  const storeAlert = appAlert();
  const storeLocation = appLocation();

  const users = ref([]);
  const userId = ref('');
  const action = ref('');
  const region = ref('');


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
      const response = await storeAuth.axiosInstance.get(`${server}/user/${userId.value}/${flag}`);
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

  /**
   * Adds a region to the server.
   *
   * @return {Promise<void>} This function does not return anything.
   */
  async function addRegion(): Promise<void> {
    const response = await storeAuth.axiosInstance.post(`${server}/region/add`, {
      'region': region.value
    });
    const  { location } = response.data;
    storeAlert.alertAttr = location ? 'alert-warning' : 'alert-success';
    storeAlert.alertText = location 
      ? 'При добавлении записи возникла ошибка'
      : 'Запись добавлена';
    storeLocation.getRegions();
  };

  /**
   * Deletes a region.
   *
   * @param {String} id - The ID of the region to be deleted.
   * @return {Promise<void>} - A promise that resolves when the region is deleted.
   */
  async function delRegion(id: String): Promise<void> {
    if (id === '1') {
      storeAlert.alertAttr = 'alert-info';
      storeAlert.alertText = 'Нельзя удалить регион "Главный офис"';
      return
    };
    if (confirm(`Вы действительно хотите удалить регион?`)) {
      const response = await storeAuth.axiosInstance.get(`${server}/region/delete/${id}`);
      const  { location } = response.data;
      
      storeAlert.alertAttr = 'alert-success';
      storeAlert.alertText = `Регион ${location} удален`;

      storeLocation.getRegions(); // Обновление списка регионов в хранилище
    }
  };
    return { users, profile, action, userId, region, getUsers, editUserInfo, submitData, viewUser, addRegion, delRegion,};
});