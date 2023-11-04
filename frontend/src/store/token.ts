import { defineStore } from 'pinia';
import { useRouter } from 'vue-router';
import { ref } from 'vue';
import axios from 'axios';
import { server } from '@share/utilities';


export const authStore = defineStore('authStore', () => {
  
  const router = useRouter();

  const refreshToken = ref(localStorage.getItem('refresh_token'));
  const accessToken = ref(localStorage.getItem('access_token'));
  
  const axiosInstance = ref(axios.create());

  axiosInstance.value.interceptors.request.use(
    async (config) => {
      if (refreshToken.value) {
        const expiry_refresh = (JSON.parse(atob(refreshToken.value.split('.')[1]))).exp;

        if (Math.floor((new Date).getTime() / 1000) >= expiry_refresh) {
          router.push({ name: 'login' });
          return Promise.reject('Refresh token expired');
        
        } else {

          if (accessToken.value) {
            const expiry_access = (JSON.parse(atob(accessToken.value.split('.')[1]))).exp;

            if (Math.floor((new Date).getTime() / 1000) >= expiry_access) {
             
              try {
                const response = await axios.post(`${server}/refresh`, null, {
                  headers: { 'Authorization': `Bearer ${localStorage.getItem('refresh_token')}` }
                });
                const { access_token } = response.data;

                if (access_token){
                  localStorage.setItem('access_token', access_token);
                  accessToken.value = access_token;

                } else {
                  router.push({ name: 'login' });
                };

              } catch (error) {
                router.push({ name: 'login' });
                return Promise.reject(error);
              }
            };
          
          } else {
            router.push({ name: 'login' });
            return Promise.reject('Access token not available');
          }
        }
      
      } else {
        router.push({ name: 'login' });
        return Promise.reject('Refresh token not available');
      }

      config.headers['Authorization'] = `Bearer ${accessToken.value}`;
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

  function setRefreshToken(token: string) {
    refreshToken.value = token;
    localStorage.setItem('refresh_token', token);
  };

  function setAccessToken(token: string){
    accessToken.value = token;
    localStorage.setItem('access_token', token);
  };

  return { 
    axiosInstance, 
    setRefreshToken, 
    setAccessToken 
  };
});
