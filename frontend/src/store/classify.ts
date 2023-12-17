import axios from 'axios';
import { ref } from 'vue';
import { defineStore } from 'pinia'
import { server } from '@utilities/utils';


export const classifyStore = defineStore('classifyStore', () => {

  const classData = ref({
    status: <Record<string, any>>({}),
    regions: <Record<string, any>>([{}]),
    conclusion: <Record<string, any>>({}),
    category: <Record<string, any>>({}),
    groups: <Record<string, any>>({}),
    roles: <Record<string, any>>({}),
    tables: Array<string>(),
    getClasses: async function (): Promise<void> {
      try {
        const response = await axios.get(`${server}/classes`);
        const {
          category,
          conclusion,
          role,
          group,
          status,
          region,
          tables
        } = response.data;
        Object.assign(classData.value, {
          category: {...category},
          conclusion: {...conclusion},
          roles: {...role},
          groups: {...group},
          status: {...status},
          regions: [...region],
          tables: tables
        })
        console.log(classData.value)
      } catch (error) {
        console.error(error)
      }
    }
  });
  return {
    classData,
  }
});
