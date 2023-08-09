import { defineStore } from 'pinia';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import server from '../store/server';

export const appAuth = defineStore('appAuth', () => {
  const refreshToken = ref(localStorage.getItem('refresh_token'));
  const accessToken = ref(localStorage.getItem('access_token'));

  const axiosInstance = ref(axios.create());
  const router = useRouter();

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
                localStorage.setItem('access_token', access_token);
                accessToken.value = access_token;
              
              } catch (error) {
                router.push({ name: 'login' });
                return Promise.reject(error);
              }
            }
          
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

  // Update the refresh token in the store
  const setRefreshToken = (token: string) => {
    refreshToken.value = token;
    localStorage.setItem('refresh_token', token);
  };

  // Update the access token in the store
  const setAccessToken = (token: string) => {
    accessToken.value = token;
    localStorage.setItem('access_token', token);
  };

  return { refreshToken, accessToken, axiosInstance, setRefreshToken, setAccessToken };
});
