import { defineStore } from 'pinia'
import { ref } from 'vue';


export const appAlert = defineStore('appAlert',  () => {

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
