import { defineStore } from 'pinia'
import { ref } from 'vue';
import axios from 'axios';
import server from '@store/server';


export const classifyStore = defineStore('classifyStore', () => {

  const status = ref<{ [key: string]: any }>({});
  const regions = ref<{ [key: string]: any }>({});
  const conclusion = ref<{ [key: string]: any }>({});
  const decision = ref<{ [key: string]: any }>({});
  const category = ref<{ [key: string]: any }>({});
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
    try {
      const response = await axios.get(`${server}/classes`);
      [ 
        status.value, 
        regions.value, 
        conclusion.value, 
        decision.value, 
        category.value, 
        groups.value, 
        roles.value 
      ] = response.data;

    } catch (error) {
      console.error(error)
    }
  };
  
  return {
    status, 
    regions,
    conclusion, 
    decision, 
    groups, 
    roles, 
    category, 
    getClassify 
  }
});
