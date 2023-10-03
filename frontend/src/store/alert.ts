import { defineStore } from 'pinia'
import { ref } from 'vue';


export const alertStore = defineStore('alertStore', () => {

  const alertAttr = ref('');
  const alertText = ref('');

  const setAlert = (attr: string = '', text: string = '') => {
    alertAttr.value = attr;
    alertText.value = text;
    
    setTimeout(() => {
      alertAttr.value = '';
      alertText.value = '';
    }, 10000);
  };

  return { alertAttr, alertText, setAlert }
})
