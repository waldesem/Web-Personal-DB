import axios from "axios";
import { ref } from "vue";
import { defineStore } from "pinia";
import { server } from "@utilities/utils";

export const classifyStore = defineStore("classifyStore", () => {
  const classData = ref({
    status: <Record<string, any>>{},
    regions: <Record<string, any>>{},
    conclusions: <Record<string, any>>{},
    roles: <Record<string, any>>{},
    users: <Record<string, any>>{},

    async getClasses(): Promise<void> {
      try {
        const response = await axios.get(`${server}/classes`);
        [
          classData.value.conclusions,
          classData.value.roles,
          classData.value.status,
          classData.value.regions,
          classData.value.users,
        ] = response.data;
      } catch (error) {
        console.error(error);
      }
    },
  });

  return {
    classData,
  };
});
