import { defineStore } from "pinia";
import { ref } from 'vue';
import { appAuth } from '@/store/auth';
import axios from 'axios';
import server from '@store/server';
import router from '@router/router';


const storeAuth = appAuth();


export const NavigationBar = defineStore('NavigationBar',  () => {
    
  const messages = ref([]);  // Список сообщений для пользователя

  let isStarted = false;  // Флаг  для проверки запуска интервала обновления

  // Получение списка сообщений после монтирования компонента и обновление каждые 10 минут
  if (!isStarted) {
    isStarted = true;
    setInterval(updateMessage, 1800000);
  };

  /**
   * Updates the messages based on the provided flag ('new' or 'reply').
   *
   * @param {string} flag - The flag to determine which messages to update. Default is 'new'.
   * @return {Promise<void>} - A promise that resolves when the message is successfully updated.
   */
  async function updateMessage(flag: string = 'new'): Promise<void> {
    try{
        const response = await storeAuth.axiosInstance.get(`${server}/messages/${flag}`);
        messages.value = response.data;
        
    } catch (error) {
        console.error(error);
    }
  };

  /**
   * Logs the user out by sending a DELETE request to the server's logout endpoint.
   *
   * @return {Promise<void>} Promise that resolves when the user is successfully logged out.
   */
  async function userLogout(): Promise<void>{
    const response = await storeAuth.axiosInstance.delete(`${server}/logout`);
    console.log(response.status);

    const resp = await axios.delete(`${server}/logout`, {
        headers: {'Authorization': `Bearer ${localStorage.getItem('refresh_token')}`}
    });
    console.log(resp.status);

    // Удаление токенов для авторизации и редирект на страницу авторизации
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');

    router.push({ name: 'login' });
  }
  return { messages, updateMessage, userLogout }
});