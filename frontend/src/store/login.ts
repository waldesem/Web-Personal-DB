import { ref } from 'vue'
import { defineStore } from 'pinia'
import { authStore } from '@/store/token';
import { alertStore } from '@store/alert';
import { classifyStore } from '@store/classify';
import { server } from '@share/utilities';
import router from '@router/router';


export const loginStore = defineStore('loginStore', () => {

  const storeAuth = authStore();
  const storeAlert = alertStore();
  const storeClasses = classifyStore();

  const pageIdentity = ref('login');

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
    Object.assign(userData, {
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

  return { 
    userData, 
    pageIdentity, 
    getAuth, 
    userLogout, 
    hasRole, 
    hasGroup
  }
});