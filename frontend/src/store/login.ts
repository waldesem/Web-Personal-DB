import router from '@router/router';
import axios from 'axios';
import server from '@store/server';
import { defineStore } from 'pinia'
import { authStore } from '@/store/token';
import { alertStore } from '@store/alert';
import { classifyStore } from '@store/classify';
import { ref } from 'vue';


export const loginStore = defineStore('loginStore', () => {

  const storeAuth = authStore();
  const storeAlert = alertStore();
  const storeClasses = classifyStore();

  const action = ref('login');
  const pageIdentity = ref('');

  const userData = ref({
    fullName: '',
    userName: '',
    userRoles: [],
    userGroups: [],
    region_id: '',
  });
  
  const loginData = ref({
    username: '',
    password: '',
    new_pswd: '',
    conf_pswd: ''
  });

  async function getAuth(): Promise<void> {
    try {
      const response = await storeAuth.axiosInstance.get(`${server}/login`);
      const userResponse = response.data;

      Object.assign(userData.value, {
        fullName: userResponse['fullname'],
        userName: userResponse['username'],
        userRoles: userResponse['roles'],
        userGroups: userResponse['groups'],
        region_id: userResponse['region_id'],
      });

      hasRole('admin')
        ? router.push({ name: 'users', params: { group: 'admins' } })
        : router.push({ name: 'persons', params: { group: userData.value.userGroups[0]['group'] } });
        storeClasses.getClassify();
        storeAlert.setAlert('', '');

    } catch (error) {
      console.error(error)
      router.push({ name: 'login' })
    }
  };

  /**
   * Submits data to the server.
   *
   * @return {Promise<void>} - A promise that resolves when the data is submitted.
   */
  async function submitLogin(): Promise<void> {
    // Проверка на совпадение паролей нового и старого
    if (action.value === 'password') {
      if (loginData.value.password === loginData.value.new_pswd) {
      storeAlert.setAlert('alert-warning', 
                          'Старый и новый пароли совпадают');
      return
      };

      // Проверка на совпадение паролей нового и подтверждения
      if (loginData.value.conf_pswd !== loginData.value.new_pswd && action.value === 'password') {
        storeAlert.setAlert('alert-warning', 
                            'Новый пароль и подтверждение не совпадают');
        return
      }
    };
    try {
      const response = action.value === 'password'
        ? await axios.patch(`${server}/login`, loginData.value)
        : await axios.post(`${server}/login`, loginData.value);
      
      const { message, access_token, refresh_token } = response.data;

      switch (message) {
        case 'Authenticated':
          if (action.value === 'password'){
            action.value = 'login';
            storeAlert.setAlert('alert-success',
                                'Пароль установлен. Войдите с новым паролем');
          } else {
            localStorage.setItem('access_token', access_token);
            localStorage.setItem('refresh_token', refresh_token);
            
            storeAuth.setRefreshToken(refresh_token);
            storeAuth.setAccessToken(access_token);
            
            getAuth();
          }
          break;
        case 'Overdue':
          action.value = 'password';
          storeAlert.setAlert('alert-warning', 
                              'Пароль просрочен. Измените пароль');
          break;

        case 'Denied':
          action.value = 'login';
          storeAlert.setAlert('alert-danger', 
                              'Неверный логин или пароль');
          break;
      }
    } catch (error) {
      console.error(error)
      storeAlert.setAlert('alert-danger', 'Ошибка авторизации');
      action.value = 'login';
      clearData();
      };
    };

  /**
   * Logs the user out by sending a GET request to the server's logout endpoint.
   *
   * @return {Promise<void>} Promise that resolves when the user is successfully logged out.
   */
  async function userLogout(): Promise<void>{
    try {
      const response = await storeAuth.axiosInstance.delete(`${server}/login`);
      console.log(response.data);

      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      router.push({ name: 'login' });
      clearData();

    } catch (error) {
      console.error(error)
    }
  };
  
  /**
   * Determines if the user has a specific role.
   *
   * @param {string} role - The role to check.
   * @return {boolean} Returns true if the user has the specified role, false otherwise.
   */
  function hasRole(role: string): boolean {
    return userData.value.userRoles.some((r: { role: any; }) => r.role === role);
  };

  /**
   * Determines if the user belongs to a specific group.
   *
   * @param {string} group - The name of the group to check.
   * @return {boolean} Returns true if the user belongs to the specified group, false otherwise.
   */
  function hasGroup(group: string): boolean {
    return userData.value.userGroups.some((g: { group: any; }) => g.group === group);
  };

  /**
   * Clears the data for login and user information.
   *
   * @return {void} No return value.
   */
  function clearData(): void {
    Object.assign(loginData.value, {
      username: '',
      password: '',
      new_pswd: '',
      conf_pswd: ''
    });

    Object.assign(userData.value, {
      fullName: '',
      userName: '',
      userRoles: [],
      userGroups: []
    })
  };

  return { 
    action, 
    userData, 
    loginData, 
    pageIdentity, 
    submitLogin, 
    getAuth, 
    userLogout, 
    hasRole, 
    hasGroup 
  }
});