import { defineStore } from 'pinia'
import { ref } from 'vue';
import axios from 'axios';
import { server } from '@share/utilities';


export const classifyStore = defineStore('classifyStore', () => {

  const classifyItems = ref({
    status: <Record<string, any>>({}),
    regions: <Record<string, any>>({}),
    conclusion: <Record<string, any>>({}),
    decision: <Record<string, any>>({}),
    category: <Record<string, any>>({}),
    groups: <Record<string, any>>({}),
    roles: <Record<string, any>>({}),
  })

  // const status = ref<{ [key: string]: any }>({});
  // const regions = ref<{ [key: string]: any }>({});
  // const conclusion = ref<{ [key: string]: any }>({});
  // const decision = ref<{ [key: string]: any }>({});
  // const category = ref<{ [key: string]: any }>({});
  // const groups = ref<{ [key: string]: any }>({});
  // const roles = ref<{ [key: string]: any }>({});
  
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
        classifyItems.value.status, 
        classifyItems.value.regions, 
        classifyItems.value.conclusion, 
        classifyItems.value.decision, 
        classifyItems.value.category, 
        classifyItems.value.groups, 
        classifyItems.value.roles 
      ] = response.data;

    } catch (error) {
      console.error(error)
    }
  };
  
  return {
    classifyItems,
    getClassify 
  }
});
