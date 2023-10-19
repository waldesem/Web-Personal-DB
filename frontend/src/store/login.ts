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

  let pageIdentity = 'login';

  let userData = {
    fullName: '',
    userName: '',
    userRoles: [],
    userGroups: [],
    region_id: '',
  };
  
  async function getAuth(): Promise<void> {
    try {
      const response = await storeAuth.axiosInstance.get(`${server}/login`);
      const userResponse = response.data;

      Object.assign(userData, {
        fullName: userResponse['fullname'],
        userName: userResponse['username'],
        userRoles: userResponse['roles'],
        userGroups: userResponse['groups'],
        region_id: userResponse['region_id'],
      });

      hasRole('admin') 
        ? router.push({ name: 'users', params: { group: 'admins' }}) 
        : router.push({ name: 'persons', params: { 
          group: userData.userGroups[0]['group'] } 
        });
      
      storeClasses.getClassify();
      storeAlert.setAlert();

    } catch (error) {
      console.error(error);
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
      console.error(error)
    };

    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    
    router.push({ name: 'login' });

    Object.assign(userData, {
      fullName: '',
      userName: '',
      userRoles: [],
      userGroups: []
    });
  };
  
  /**
   * Determines if the user has a specific role.
   *
   * @param {string} role - The role to check.
   * @return {boolean} Returns true if the user has the specified role, false otherwise.
   */
  function hasRole(role: string): boolean {
    return userData.userRoles.some((r: { role: any; }) => r.role === role);
  };

  /**
   * Determines if the user belongs to a specific group.
   *
   * @param {string} group - The name of the group to check.
   * @return {boolean} Returns true if the user belongs to the specified group, false otherwise.
   */
  function hasGroup(group: string): boolean {
    return userData.userGroups.some((g: { group: any; }) => g.group === group);
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