import axios from "axios";
import { ref } from "vue";
import { defineStore } from "pinia";
import { server, reduceItems } from "@utilities/utils";

export const classifyStore = defineStore("classifyStore", () => {
  const classData = ref({
    status: <Record<string, any>>[{}],
    regions: <Record<string, any>>[{}],
    conclusion: <Record<string, any>>[{}],
    roles: <Record<string, any>>{},

    async getClasses(): Promise<void> {
      try {
        const response = await axios.get(`${server}/classes`);
        const { conclusion, role, status, region } = response.data;

        Object.assign(classData.value, {
          conclusion: reduceItems(conclusion, "conclusion"),
          status: reduceItems(status, "status"),
          regions: reduceItems(region, "region"),
          roles: role,
        });
      } catch (error) {
        console.error(error);
      }
    },
  });

  return {
    classData,
  };
});
