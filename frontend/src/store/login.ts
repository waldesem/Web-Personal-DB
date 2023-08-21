import axios from 'axios';
import { ref } from 'vue';
import { defineStore } from 'pinia'
import { appAuth } from '@store/auth';
import { appAlert } from '@store/alert';
import { appLocation } from '@store/location';
import { appClassify } from '@store/classify';
import server from '@store/server';
import router from '@router/router';


const storeAuth = appAuth();

const storeAlert = appAlert();

const storeLocation = appLocation();

const classifyApp = appClassify();


export const appLogin = defineStore('appLogin',  () => {

  const action = ref('login');

  const fullName = ref('');

  const userName = ref('');

  const userRole = ref('');
  
  // Объект с данными из формы входа пользователя
  const loginData = ref({
    username: '',
    password: '',
    new_pswd: '',
    conf_pswd: ''
  });

  storeAlert.alertAttr = 'alert-info';
  storeAlert.alertText = 'Авторизуйтесь для входа в систему';


  async function getAuth(): Promise<void> {
    try {
      const response = await storeAuth.axiosInstance.get(`${server}/auth`);
      const { access, fullname, username, role } = response.data;
      
      access === "Authorized" 
      ? router.push({ name: 'persons' })
      : router.push({ name: 'login' });
      
      fullName.value = fullname;
      userName.value = username;
      userRole.value = role;
  
      storeLocation.getRegions();  // Получение списка регионов
      classifyApp.getClassify();  // Получение списка категорий
    
    } catch (error) {
      console.error(error)
      router.push({ name: 'login' })
    }
  }

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
      const { access, access_token, refresh_token, fullname, username, role } = response.data;

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

          fullName.value = fullname;
          userName.value = username;
          userRole.value = role;

          storeLocation.getRegions();  // Получение списка регионов
          classifyApp.getClassify();  // Получение списка категорий

          router.push({ name: 'persons' });
          break;

        case "Overdue":
          // Пароль просрочен
          action.value = 'password';
          storeAlert.alertAttr = 'alert-warning';
          storeAlert.alertText = 'Пароль просрочен. Измените пароль';
          storeAuth.setRefreshToken(refresh_token);
          storeAuth.setAccessToken(access_token);
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
  }

  return { action, fullName, userName, userRole, loginData, submitData, getAuth }
})