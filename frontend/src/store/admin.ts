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
  const selectRole = ref('');
  const selectGroup = ref('');

  interface Group {
    id: string,
    group: string
  };

  interface Role {
    id: string,
    role: string
  };

  interface User {
    id: string,
    fullname: string,
    username: string,
    email: string,
    region_id: string,
    pswd_create: string,
    pswd_change: string,
    last_login: string,
    roles: Role[],
    groups: Group[],
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
  async function userAction(action: String, id: string = userId.value): Promise<void>{
    try {
      const response = await storeAuth.axiosInstance.get(`${server}/user/${action}/${id}`);
      profile.value = response.data;
      
      if (action !== 'view') {
        const resp = {
          'block': ['alert-success', 'Пользователь (за/раз)блокирован'],
          'drop': ['alert-success', 'Пароль пользователя удален']
        };
        storeAlert.setAlert(resp[action as keyof typeof resp][0],
                            resp[action as keyof typeof resp][1]);
      };

    } catch (error) {
      console.error(error);
    }
  };

  async function userDelete(): Promise<void>{
    if (confirm("Вы действительно хотите удалить пользователя?")){
      try {
        const response = await storeAuth.axiosInstance.delete(`${server}/user/${userId.value}`);
        console.log(response.status);

        storeAlert.setAlert('alert-danger', 'Пользователь удалён');
        router.push({ name: 'users', params: { group: 'admins' } });

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
  async function submitUserData(): Promise<void>{
    const formData = {
      'fullname': profile.value.fullname,
      'username': profile.value.username,
      'email': profile.value.email,
      'region_id': profile.value.region_id,
    };
    try {  
      const response = action.value === 'edit' 
        ? await storeAuth.axiosInstance.patch(`${server}/user`, formData)
        : await storeAuth.axiosInstance.post(`${server}/user`, formData);
      const { message } = response.data;

      const resp = {
        'Created': ['alert-success', 'Пользователь успешно создан'],
        'Patched': ['alert-success', 'Пользователь успешно изменен'],
      }
      storeAlert.setAlert(resp[message as keyof typeof resp][0],
                          resp[message as keyof typeof resp][1]);
      action.value === 'edit' ? userAction('view', userId.value): getUsers();
      action.value = '';

    } catch (error) {
      console.error(error);
      storeAlert.setAlert('alert-danger', 'Ошибка сохранения данных');
    }
  };

  /**
   * Edits the group role.
   *
   * @return {Promise<void>} Promise that resolves when the function completes.
   */
  async function editGroupRole(
    item: string, action: string, value: string = ''
    ): Promise<void> {
    
    value = item === 'role' ? selectRole.value : selectGroup.value;
    
    try {
      const response = action == 'add' 
        ? await storeAuth.axiosInstance.get(
          `${server}/${item}/${value}/${userId.value}`
          )
        : await storeAuth.axiosInstance.delete(
          `${server}/${item}/${value}/${userId.value}`
          );

      const result = response.status;
      if (result === 201 || result === 204) {
        const flags = {
          'role': 'Роль',
          'group': 'Группа'
        };
        const actions = {
          'add': ['alert-success', item === 'role' 
            ? `Пользователю ${userId.value} добавлена \
            ${flags[item as keyof typeof flags]} ${value}` 
            : `Пользователь ${userId.value} добавлен в: \
            ${flags[item as keyof typeof flags]} ${value}`],
          'remove': ['alert-info', item === 'role' 
            ? `Пользователю ${userId.value} удалена \
            ${flags[item as keyof typeof flags]} ${value}`
            : `Пользователь ${userId.value} удален из: \
            ${flags[item as keyof typeof flags]} ${value}`]
        };
      
        storeAlert.setAlert(actions[action as keyof typeof actions][0], 
                            actions[action as keyof typeof actions][1]);

        userAction('view', userId.value);
      }
    } catch (error) {
    console.error(error);
    storeAlert.setAlert('alert-danger', 
                        'Роль уже добавлена или пользователь уже включён в группу');
    }
  };
  
  return { users, profile, action, userId, flag, selectRole, selectGroup,
    getUsers, submitUserData, userAction, userDelete, editGroupRole };
});