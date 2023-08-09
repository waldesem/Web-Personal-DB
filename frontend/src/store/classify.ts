import { defineStore } from 'pinia'
import axios from 'axios';
import server from '../store/server';
import { ref } from 'vue';


export const appClassify = defineStore('appClassify',  () => {

  const status = ref<{ [key: string]: any }>({});
  const role = ref({});
  const conclusion = ref({});
  const decision = ref({});
  const category = ref({});

  async function getClassify() {
    const response = await axios.get(`${server}/classify`);
    const [statuses, roles, conclusions, decisions, categories] = response.data;

    status.value = statuses; 
    role.value = roles;
    conclusion.value = conclusions; 
    decision.value = decisions;
    category.value = categories;
  }
  
  return { status, role, conclusion, decision, category, getClassify }
})
