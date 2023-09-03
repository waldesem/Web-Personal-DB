import { defineStore } from 'pinia'
import axios from 'axios';
import server from '../store/server';
import { ref } from 'vue';


export const appClassify = defineStore('appClassify',  () => {

  const status = ref<{ [key: string]: any }>({});
  const regions = ref<{ [key: string]: any }>({});
  const conclusion = ref({});
  const decision = ref({});
  const category = ref({});
  const groups = ref({});
  const roles = ref({});
  
  async function getClassify() {
    const response = await axios.get(`${server}/classify`);
    const [statuses, region, conclusions, decisions, categories, group, role] = response.data;

    status.value = statuses; 
    regions.value = region;
    conclusion.value = conclusions; 
    decision.value = decisions;
    category.value = categories;
    groups.value = group;
    roles.value = role;
  };
  
  return { status, regions, conclusion, decision, groups, roles, category, getClassify }
})
