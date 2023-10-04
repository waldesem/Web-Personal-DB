import { defineStore } from 'pinia';
import { ref } from 'vue';


export const alertStore = defineStore('alertStore', () => {

  const attrAlert = ref('');
  const textAlert = ref('');

  const setAlert = (attr: string = '', text: string = '') => {
    attrAlert.value = attr;
    textAlert.value = text;
    
    setTimeout(() => {
      setAlert();
    }, 10000);
  };

  return { 
    attrAlert, 
    textAlert, 
    setAlert 
  }
})
