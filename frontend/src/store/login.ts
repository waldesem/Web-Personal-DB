import router from '@router/router';
import axios from 'axios';
import server from '@store/server';
import { defineStore } from 'pinia'
import { appAuth } from '@/store/token';
import { appAlert } from '@store/alert';
import { appClassify } from '@store/classify';
import { ref } from 'vue';


export const appLogin = defineStore('appLogin', () => {

  const storeAuth = appAuth();
  const storeAlert = appAlert();
  const classifyApp = appClassify();

  const action = ref('login');
  const pageIdentity = ref('');

  const userData = ref({
    fullName: '',
    userName: '',
    userRoles: [],
    userGroups: []
  });
  
  // Объект с данными из формы входа пользователя
  const loginData = ref({
    username: '',
    password: '',
    new_pswd: '',
    conf_pswd: ''
  });

  async function getAuth(): Promise<void> {
    try {
      const response = await storeAuth.axiosInstance.get(`${server}/auth`);
      const { access, fullname, username, roles, groups } = response.data;

      Object.assign(userData.value, {
        fullName: fullname,
        userName: username,
        userRoles: roles,
        userGroups: groups
      });

      if (access === "Denied") {
        router.push({ name: 'login' });
      } else {
        hasRole('admin')
          ? router.push({ name: 'users', params: { group: 'admins' } })
          : router.push({ name: 'persons', params: { group: userData.value.userGroups[0]['group'] } });
          classifyApp.getClassify();  // Получение списка категорий
      };

    } catch (error) {
      console.error(error)
      router.push({ name: 'login' })
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
   * Submits data to the server.
   *
   * @return {Promise<void>} - A promise that resolves when the data is submitted.
   */
  async function submitData(): Promise<void> {
  // Проверка на совпадение паролей нового и старого
    if (action.value === 'password') {
      if (loginData.value.password === loginData.value.new_pswd) {
      storeAlert.alertAttr = 'alert-warning';
      storeAlert.alertText = 'Старый и новый пароли совпадают';
      return
      };
      // Проверка на совпадение паролей нового и подтверждения
      if (loginData.value.conf_pswd !== loginData.value.new_pswd && action.value === 'password') {
        storeAlert.alertAttr = 'alert-warning';
        storeAlert.alertText = 'Новый пароль и подтверждение не совпадают';
        return
      }
    };
    try {
      const response = action.value === 'password'
      ? await axios.post(`${server}/password`, loginData.value)
      : await axios.post(`${server}/login`, loginData.value);
      const { access, access_token, refresh_token, fullname, username, roles, groups } = response.data;

      switch (access) {
        case "Success":
          // Успешная смена пароля
          action.value = 'login';
          storeAlert.alertAttr = 'alert-success';
          storeAlert.alertText = 'Пароль установлен. Войдите с новым паролем';
          break;

        case "Authorized":
          // Успешная авторизация, сохранение токенов и перенаправление на главную страницу
          localStorage.setItem('access_token', access_token);
          localStorage.setItem('refresh_token', refresh_token);

          storeAuth.setRefreshToken(refresh_token);
          storeAuth.setAccessToken(access_token);

          Object.assign(userData.value, {
            fullName: fullname,
            userName: username,
            userRoles: roles,
            userGroups: groups
          });
          classifyApp.getClassify();  // Получение списка категорий

          hasRole('admin')
            ? router.push({ name: 'users', params: { group: 'admins' } })
            : router.push({ name: 'persons', params: { group: userData.value.userGroups[0]['group'] } });
          storeAlert.setAlert('alert-success', 'Успешный вход в систему');
          break;

        case "Overdue":
          // Пароль просрочен
          action.value = 'password';
          storeAlert.alertAttr = 'alert-warning';
          storeAlert.alertText = 'Пароль просрочен. Измените пароль';
          break;

        case "Denied":
          // Неверный логин или пароль
          action.value = 'login';
          storeAlert.alertAttr = 'alert-danger';
          storeAlert.alertText = 'Неверный логин или пароль';
          break;
      }
    } catch (error) {
      console.error(error)
    }
  };

  /**
   * Logs the user out by sending a GET request to the server's logout endpoint.
   *
   * @return {Promise<void>} Promise that resolves when the user is successfully logged out.
   */
  async function userLogout(): Promise<void>{
    const response = await storeAuth.axiosInstance.get(`${server}/logout`);
    console.log(response.status);

    // Удаление токенов для авторизации и редирект на страницу авторизации
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    
    router.push({ name: 'login' });
  };
  
  return { action, userData, loginData, pageIdentity, submitData, getAuth, userLogout, hasRole, hasGroup }
})