import axios from 'axios';
import { ref } from 'vue';
import { defineStore } from 'pinia'
import { server } from '@share/utilities';


export const classifyStore = defineStore('classifyStore', () => {

  const classData = ref({
    status: <Record<string, any>>({}),
    regions: <Record<string, any>>({}),
    conclusion: <Record<string, any>>({}),
    decision: <Record<string, any>>({}),
    category: <Record<string, any>>({}),
    groups: <Record<string, any>>({}),
    roles: <Record<string, any>>({}),
    tables: <Record<string, any>>({}),
    getClasses: async function (): Promise<void> {
      try {
        const response = await axios.get(`${server}/classes`);
        [ 
          this.status, 
          this.regions, 
          this.conclusion, 
          this.decision, 
          this.category, 
          this.groups, 
          this.roles,
          this.tables
        ] = response.data;
      } catch (error) {
        console.error(error)
      }
    }
  });
  return {
    classData,
  }
});
