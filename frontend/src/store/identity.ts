import { ref } from 'vue'
import { defineStore } from 'pinia'


export const identityStore = defineStore('identityStore', () => {

  const pageIdentity = ref('')

  return {pageIdentity}
});
