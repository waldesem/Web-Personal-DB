import { defineStore } from 'pinia';
import { ref } from 'vue'
import { authStore } from '@/store/token';
import { alertStore } from '@store/alert';
import { server } from '@store/shared';


export const adminStore = defineStore('adminStore', () => {

  const storeAuth = authStore();
  const storeAlert = alertStore();

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

  const userData = ref({
    userList: <User[]>([]),
    userId: '',
    userAct: '',
    userFlag: '',
    userRole: '',
    userGroup: '',
    currentPage: 1,
    hasNext: false,
    hasPrev: false,
  });

  const profileData = ref<User>({
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
      userData.value.userList = response.data;
    
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
  async function userAction(action: String, id: string = userData.value.userId): Promise<void>{
    try {
      const response = await storeAuth.axiosInstance.get(`${server}/user/${action}/${id}`);
      profileData.value = response.data;
      
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
      userAction('view', userData.value.userId);
    }
  };

  return { 
    userData, 
    profileData, 
    getUsers, 
    userAction
  };
});
