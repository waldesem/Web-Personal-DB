import { defineStore } from 'pinia';
import { appAuth } from '@/store/token';
import { ref } from 'vue';
import server from '@/store/server';

export const appMessages = defineStore('appMessages', () => {
  
  const storeAuth = appAuth();
  const messages = ref([]);  // Список сообщений для пользователя

  // Получение списка сообщений после монтирования компонента и обновление каждые 30 минут
  let isStarted = false;
  if (!isStarted) {
    updateMessage();
    isStarted = true;
    setInterval(updateMessage, 1000000);
  };

  /**
   * Updates the messages based on the provided flag ('new' or 'reply').
   *
   * @param {string} flag - The flag to determine which messages to update. Default is 'new'.
   * @return {Promise<void>} - A promise that resolves when the message is successfully updated.
   */
  async function updateMessage(flag: string = 'new'): Promise<void> {
    try {
      const response = await storeAuth.axiosInstance.get(`${server}/messages/${flag}`);
      messages.value = response.data;
        
    } catch (error) {
        console.error(error);
    }
  };

  return { messages, updateMessage };
});
