import { defineStore } from 'pinia'
import { ref } from 'vue';


export const appUsers = defineStore('appUsers',  () => {

  const fullName = ref('');
  const userName = ref('');

  return { fullName, userName }
})
