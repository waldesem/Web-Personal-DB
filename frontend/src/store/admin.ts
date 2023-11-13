import { defineStore } from 'pinia';
import { ref } from 'vue'
import { authStore } from '@/store/token';
import { server } from '@share/utilities';
import { User } from '@share/interfaces';


export const adminStore = defineStore('adminStore', () => {

  const storeAuth = authStore();

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

  const formData = ref({
    fullname: '',
    username: '',
    email: '',
    region_id: '',
  });

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
    userData.value.userId = id;
    try {
      const response = await storeAuth.axiosInstance.get(`${server}/user/${action}/${id}`);
      profileData.value = response.data;
      
    } catch (error) {
      console.error(error);
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
