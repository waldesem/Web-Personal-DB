import axios from "axios";
import { ref } from "vue";
import { defineStore } from "pinia";
import { server } from "@utilities/utils";

export const classifyStore = defineStore("classifyStore", () => {

  const classData = ref({
    status: <Record<string, any>>{},
    regions: <Record<string, any>>[{}],
    conclusion: <Record<string, any>>{},
    roles: <Record<string, any>>{},

    getClasses: async function (): Promise<void> {
      try {
        const response = await axios.get(`${server}/classes`);
        const { conclusion, role, status, region } =
          response.data;

        Object.assign(classData.value, {
          conclusion: this.reduceItems(conclusion, "conclusion"),
          status: this.reduceItems(status, "status"),
          regions: this.reduceItems(region, "region"),
          roles: role,
        });
      } catch (error) {
        console.error(error);
      }
    },

    reduceItems: function (
      items: Record<string, any>,
      value: string
    ): Record<string, any> {
      return items.reduce(
        (
          acc: { [x: string]: any },
          item: { id: string | number; [x: string]: any }
        ) => {
          acc[item.id] = item[value];
          return acc;
        },
        {} as { [key: string]: string }
      );
    },
  });
  
  return {
    classData,
  };
});
