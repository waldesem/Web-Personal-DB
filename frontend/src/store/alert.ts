import { defineStore } from 'pinia'
import { ref } from 'vue';


export const appAlert = defineStore('appAlert',  () => {

  const alertAttr = ref('');
  const alertText = ref('');

  return { alertAttr, alertText }
})
