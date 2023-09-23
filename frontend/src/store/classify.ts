import { defineStore } from 'pinia'
import { ref } from 'vue';
import axios from 'axios';
import server from '@store/server';


export const appClassify = defineStore('appClassify', () => {

  const status = ref<{ [key: string]: any }>({});
  const regions = ref<{ [key: string]: any }>({});
  const conclusion = ref({});
  const decision = ref({});
  const category = ref({});
  const groups = ref<{ [key: string]: any }>({});
  const roles = ref<{ [key: string]: any }>({});
  
  /**
   * Retrieves the classification data from the server
   * and updates the corresponding variables with the response.
   *
   * @return {Promise<void>} A promise that resolves once the data 
   * is retrieved and variables are updated.
   */
  async function getClassify(): Promise<void> {
    const response = await axios.get(`${server}/classes`);
    const [statuses, region, conclusions, 
      decisions, categories, group, role] = response.data;

    status.value = statuses; 
    regions.value = region;
    conclusion.value = conclusions; 
    decision.value = decisions;
    category.value = categories;
    groups.value = group;
    roles.value = role;
  };
  
  return { status, regions, conclusion, decision, 
    groups, roles, category, getClassify }
})
