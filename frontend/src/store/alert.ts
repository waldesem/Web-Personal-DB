import { defineStore } from 'pinia';
import { ref } from 'vue';
import { Message } from '@share/interfaces'

export const alertStore = defineStore('alertStore', () => {

  const alertMessage = ref<Message>({
    attrAlert: '',
    textAlert: ''
  });

  const setAlert = (attr: string = '', text: string = '') => {
    alertMessage.value.attrAlert = attr;
    alertMessage.value.textAlert = text;
    
    setTimeout(() => {
      setAlert();
    }, 10000);
  };

  return { 
    alertMessage, 
    setAlert 
  }
})
