import { defineStore } from 'pinia';
import { ref } from 'vue';
import { authStore } from '@store/token';
import { server } from '@share/utilities'

export const messageStore = defineStore('messageStore', () => {

  const storeAuth = authStore();

  const messages = ref([]);

    /**
   * Updates the messages based on the provided flag ('new' or 'reply').
   *
   * @param {string} flag - The flag to determine which messages to update. Default is 'new'.
   * @return {Promise<void>} - A promise that resolves when the message is successfully updated.
   */
  async function updateMessages(flag: string = 'new'): Promise<void> {
    try {
      const response = flag === 'new' 
        ? await storeAuth.axiosInstance.get(`${server}/messages`)
        : await storeAuth.axiosInstance.delete(`${server}/messages`);
      messages.value = response.data;
        
    } catch (error) {
      console.error(error);
    }
  };

  return { 
    messages,
    updateMessages, 
  }
});

