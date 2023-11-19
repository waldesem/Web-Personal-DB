import axios from 'axios';
import { ref } from 'vue'
import { defineStore } from 'pinia'
import { authStore } from '@/store/token';
import { alertStore } from '@store/alert';
import { classifyStore } from '@store/classify';
import { server, clearItem } from '@share/utilities';
import router from '@router/router';


export const loginStore = defineStore('loginStore', () => {

  const storeAuth = authStore();
  const storeAlert = alertStore();
  const storeClasses = classifyStore();
  const storeLogin = loginStore();

  const pageIdentity = ref('login');

  const formData = ref({
    data: <Record<string, any>>{},
    action: 'login',
    password: false,
  });

  const userData = ref({
    fullName: '',
    userName: '',
    userRoles: [],
    userGroups: [],
    region_id: '',
  });
  
  async function getAuth(): Promise<void> {
    
    try {
      const response = await storeAuth.axiosInstance.get(`${server}/login`);
      const { fullname, username, roles, groups, region_id } = response.data;

      assignUserData(fullname, username, roles, groups, region_id);

      hasRole('admin') 
        ? router.push({ name: 'users', params: { 
          group: 'admins' 
        }
      }) 
        : router.push({ name: 'persons', params: {
          group: userData.value.userGroups[0]['group'] 
        }
      });
      
      storeClasses.getClassify();
      storeAlert.setAlert();

    } catch (error) {
      storeAlert.setAlert('alert-warning', error as string);
      userLogout();
    }
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

    } catch (error) {
      storeAlert.setAlert('alert-warning', error as string);
    };

    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    
    assignUserData();

    router.push({ name: 'login' });
  };
  
  function assignUserData (name='', user='', roles=[], groups=[], id='') {
    Object.assign(userData.value, {
      fullName: name,
      userName: user,
      userRoles: roles,
      userGroups: groups,
      region_id: id
    });
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
  async function submitLogin(): Promise<void> {

    if (formData.value.action === 'password') {
      if (formData.value['password'] === formData.value.data['new_pswd']) {
        storeAlert.setAlert('alert-warning', 'Старый и новый пароли совпадают');
        return
      };
      if (formData.value.data['conf_pswd'] !== formData.value.data['new_pswd']) {
        storeAlert.setAlert('alert-warning', 'Новый пароль и подтверждение не совпадают');
        return
      }
    };
    try {
      const response = formData.value.action === 'password'
        ? await axios.patch(`${server}/login`, formData.value.data)
        : await axios.post(`${server}/login`, formData.value.data);
      const { message, access_token, refresh_token } = response.data;
      
      switch (message) {
        case 'Authenticated':
          if (formData.value.action === 'password') {
            formData.value.action = 'login';
            storeAlert.alertMessage.attrAlert = 'alert-success';
            storeAlert.alertMessage.textAlert = 'Войдите с новым паролем';
            clearItem(formData.value)
            
          } else {          
            localStorage.setItem('refresh_token', refresh_token);
            localStorage.setItem('access_token', access_token);
            storeLogin.getAuth();
          };
          break;

        case 'Overdue':
          formData.value.action = 'password';
          storeAlert.setAlert('alert-warning', 'Пароль просрочен. Измените пароль');
          break;

        case 'Denied':
          formData.value.action = 'login';
          storeAlert.setAlert('alert-danger', 'Неверный логин или пароль');
          break;
      };
    } catch (error) {
      storeAlert.setAlert('alert-warning', error as string);
      storeLogin.userLogout();
      clearItem(formData.value)
    };
  };


  return { 
    userData, 
    pageIdentity,
    formData,
    getAuth, 
    userLogout, 
    hasRole, 
    hasGroup,
    submitLogin
  }
});