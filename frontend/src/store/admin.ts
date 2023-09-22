import { defineStore } from 'pinia';
import { ref } from 'vue'
import { appAuth } from '@/store/token';
import { appAlert } from '@store/alert';
import router from '@router/router';
import server from '@store/server';


export const storeAdmin = defineStore('storeAdmin', () => {

  const storeAuth = appAuth();
  const storeAlert = appAlert();

  const users = ref<User[]>([]);
  const userId = ref('');
  const action = ref('');
  const flag = ref('');
  const orRoleGroup = ref('');

  interface User {
    id: string,
    fullname: string,
    username: string,
    email: string,
    region_id: string,
    pswd_create: string,
    pswd_change: string,
    last_login: string,
    roles: string[],
    groups: string[],
    blocked: string,
    attempt: string
  };

  const profile = ref<User>({
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

  /**
   * Retrieves a list of users from the server.
   *
   * @return {Promise<void>} - A promise that resolves with the list of users 
   * retrieved from the server.
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
   * Fetches user data from the server based on the provided ID 
   * and updates the profile value.
   *
   * @param {String} id - The ID of the user to fetch data for.
   * @return {Promise<void>} - A promise that resolves when the user data 
   * is fetched and the profile value is updated.
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
   * @return {Promise<void>} - A promise that resolves when the user information 
   * has been edited.
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
      storeAlert.setAlert(resp[user as keyof typeof resp][0],
                          resp[user as keyof typeof resp][1]);
      // Обновление страницы либо редирект на страницу списка пользователей
      user !== 'delete' ? viewUser(userId.value) : router.push({ name: 'users', params: { group: 'admins' } });
      
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
      });
      const  { user } = response.data;
      // Матчинг атрибута и текста сообщения
      const resp = {
        'create': ['alert-success', 'Пользователь успешно создан'],
        'edit': ['alert-success', 'Пользователь успешно изменен'],
        'none': ['alert-danger', 'Ошибка создания (пользователь существует)/редактирования']
      }
      storeAlert.setAlert(resp[user as keyof typeof resp][0],
                          resp[user as keyof typeof resp][1]);
      action.value === 'create' ? getUsers() : viewUser(userId.value);
      action.value = '';

    } catch (error) {
      console.error(error);
    }
  };

  function resetItem(){
    Object.keys(profile.value).forEach((key: string) => {
      delete profile.value[key as keyof typeof profile.value];
    });
  };

  /**
   * Edits the group role.
   *
   * @return {Promise<void>} Promise that resolves when the function completes.
   */
  async function editGroupRole(item: string, choice: string, value: string = orRoleGroup.value): Promise<void> {
    if (value) {
      try {
        const response = await storeAuth.axiosInstance.get(`${server}/admin/${item}/${choice}/${value}/${userId.value}`);
        const { result } = response.data;
        if (result === 'Success') {
          // Матчинг атрибута и текста сообщения
          const flags = {
            'role': 'Роль',
            'group': 'Группа'
          };
          const actions = {
            'add': ['alert-success', item === 'role' 
              ? `Пользователю ${userId.value} добавлена ${flags[item as keyof typeof flags]} ${value}` 
              : `Пользователь ${userId.value} добавлен в: ${flags[item as keyof typeof flags]} ${value}`],
            'remove': ['alert-info', item === 'role' 
              ? `Пользователю ${userId.value} удалена ${flags[item as keyof typeof flags]} ${value}`
              : `Пользователь ${userId.value} удален из: ${flags[item as keyof typeof flags]} ${value}`]
          };
        
          // Обновление сообщения
          storeAlert.setAlert(actions[choice as keyof typeof actions][0], 
                              actions[choice as keyof typeof actions][1]);
          // Обновление профиля
          viewUser(userId.value)
        } else if (result === 'Failed') {
          storeAlert.setAlert('alert-danger', 'Роль уже добавлена или пользователь уже включён в группу');
        } else {
          storeAlert.setAlert('alert-danger', 'Ошибка');
        }

      } catch (error) {
      console.error(error);
      }
    }
  };

  return { users, profile, action, userId, flag, orRoleGroup, 
    getUsers, editUserInfo, submitData, viewUser, resetItem, editGroupRole };
});