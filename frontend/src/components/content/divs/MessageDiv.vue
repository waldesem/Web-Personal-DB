<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { authStore } from "@store/auth";
import { server, timeSince } from "@utilities/utils";
import { Message } from "@/interfaces/interface";

const TableSlots = defineAsyncComponent(
  () => import("@components/content/elements/TableSlots.vue")
);

const storeAuth = authStore();

onBeforeMount(() => {
  messageData.value.updateMessages();
});

const messageData = ref({
  isStarted: false,
  messages: Array<Message>(),

  async updateMessages(): Promise<void> {
    try {
      const response = await storeAuth.axiosInstance.get(
        `${server}/messages`
      );
      const { messages } = response.data;
      this.messages = messages;
    } catch (error) {
      console.error(error);
    }
    if (!this.isStarted) {
      this.isStarted = true;
      setInterval(this.updateMessages, 1000000);
    }
  },

  async deleteMessage(): Promise<void> {
    try {
      const response = await storeAuth.axiosInstance.delete(
        `${server}/messages`
      );
      console.log(response.status);
      this.updateMessages();
    } catch (error) {
      console.error(error);
    }
  },
});
</script>

<template>
  <a 
    href="#offcanvasMessage"
    role="button"
    data-bs-toggle="offcanvas"
  >
  <i class="fs-3" 
    :class="`${messageData.messages.length ? 'bi bi-bell-fill' : 'bi bi-bell'}`"></i>
    <span
      v-if="messageData.messages.length"
      class="position-absolute translate-middle badge rounded-pill text-bg-success"
    >
      {{ messageData.messages.length }}
    </span>
  </a>
  <div class="offcanvas offcanvas-end" data-bs-scroll="true" id="offcanvasMessage">
    <div class="offcanvas-body">
      <TableSlots>
        <template v-slot:thead>
          <tr>
            <th>Дата</th>
            <th>Сообщение</th>
          </tr>
        </template>
        <template v-slot:tbody>
          <tr v-for="message, index in messageData.messages" :key="index">
            <td width="30%">
              {{ timeSince(message["created"]) }}</td>
            <td>{{ message["message"] }}</td>
          </tr>
          <tr><td colspan="2">
            <a href="#" class="link-danger" @click="messageData.deleteMessage()">
              Удалить сообщения
            </a>
          </td></tr>
        </template>
      </TableSlots>
     
    </div>
  </div>
</template>

<style scoped>
.offcanvas {
  min-height: auto;
  max-width: 50vh;
  overflow-y: auto;
}
</style>