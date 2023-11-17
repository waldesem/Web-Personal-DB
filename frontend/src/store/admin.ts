import { defineStore } from 'pinia';
import { ref } from 'vue'
import { authStore } from '@/store/token';
import { alertStore } from '@store/alert';
import { server } from '@share/utilities';
import { User } from '@share/interfaces';


export const adminStore = defineStore('adminStore', () => {

  const storeAuth = authStore();
  const storeAlert = alertStore();

  const userData = ref({
    userList: <User[]>([]),
    userId: '',
    userAct: '',
    userFlag: '',
    userRole: '',
    userGroup: '',
    searchUser: ''
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

  const formData: Record<string, any> = ref({});

  /**
   * Retrieves a list of users from the server.
   *
   * @return {Promise<void>} - A promise that resolves with the list of users 
   * retrieved from the server.
   */
  async function getUsers(): Promise<void>{
    try {
      const response = await storeAuth.axiosInstance.post(`${server}/users`,
      {
        'fullname': userData.value.searchUser 
      });
      userData.value.userList = response.data;
    
    } catch (error) {
      storeAlert.setAlert('alert-success', error as string)
    }
  };

  async function userAction(action: String): Promise<void>{
    try {
      const response = await storeAuth.axiosInstance.get(
        `${server}/user/${action}/${userData.value.userId}`
        );
      profileData.value = response.data;

      if (action === 'drop'){
        storeAlert.setAlert('alert-success', 'Пароль сброшен');
      } else if (action === 'block') {
        storeAlert.setAlert('alert-success', 
          `Пользователь ${profileData.value.blocked ? 'разблокирован' : 'заблокирован'}`);
      };
    } catch (error) {
      storeAlert.setAlert('alert-success', error as string)
    }
  };

  return {
    formData,
    userData, 
    profileData, 
    getUsers, 
    userAction
  };
});
