import { defineStore } from "pinia";
import { ref } from "vue";
import { authStore } from "@store/token";
import { server } from "@utilities/utils";

export const messageStore = defineStore("messageStore", () => {
  const storeAuth = authStore();

  const messageData = ref({
    messages: [],
    hasPrev: false,
    hasNext: false,
    currentPage: 1,

    updateMessages: async function (
      action: string = "new",
      page: number = 1
    ): Promise<void> {
      try {
        const response = await storeAuth.axiosInstance.get(
          `${server}/messages/${page}`,
          {
            params: { action: action },
          }
        );

        const [datas, metadata] = response.data;

        if (action === "read") {
          this.updateMessages("all");
        } else {
          this.messages = datas;
          this.hasPrev = metadata.has_prev;
          this.hasNext = metadata.has_next;
        }
      } catch (error) {
        console.error(error);
      }
    },
    deleteMessage: async function (): Promise<void> {
      try {
        const response = await storeAuth.axiosInstance.delete(
          `${server}/messages`
        );
        console.log(response.status);
        this.updateMessages("all");
      } catch (error) {
        console.error(error);
      }
    },
  });

  return {
    messageData,
  };
});
