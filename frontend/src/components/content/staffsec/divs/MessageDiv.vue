<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { authStore } from "@store/auth";
import { server } from "@utilities/utils";
import { Message } from "@/interfaces/interface";

const TableSlots = defineAsyncComponent(
  () => import("@components/elements/TableSlots.vue")
);

const storeAuth = authStore();

onBeforeMount(() => {
  messageData.value.updateMessages();
});

const messageData = ref({
  isStarted: false,
  messages: Array<Message>(),

  updateMessages: async function (): Promise<void> {
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

  deleteMessage: async function (): Promise<void> {
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
  <li 
    class="nav-item"
    :class="{'dropdown' : messageData.messages.length}">
    <a v-if="messageData.messages.length"
      href="#"
      class="nav-link active dropdown-toggle"
      role="button"
      data-bs-toggle="dropdown"
      data-bs-auto-close="outside"
    >
      Сообщения
      <span
        class="position-absolute translate-middle badge rounded-pill text-bg-success"
      >
        {{ messageData.messages.length }}
      </span>
    </a>
    <a v-else class="nav-link">Сообщения</a>
    <div :class="{'dropdown-menu' : messageData.messages.length}">
      <div v-if="messageData.messages.length" class="dropdown-item">
        <TableSlots>
          <template v-slot:thead>
            <tr>
              <th width="30%">Дата</th>
              <th>Сообщение</th>
            </tr>
          </template>
          <template v-slot:tbody>
            <tr v-for="message, index in messageData.messages" :key="index">
              <td width="30%">
                {{ new Date(String(message["created"])).toLocaleString('ru-RU') }}</td>
              <td>{{ message["message"] }}</td>
            </tr>
          </template>
        </TableSlots>
        <a href="#" class="link-danger" @click="messageData.deleteMessage()">
          Удалить сообщения
        </a>
      </div>
    </div>
  </li>
</template>

<style scoped>
.dropdown-menu {
  min-height: auto;
  max-height: 75vh;
  min-width: auto;
  max-width: 50vh;
  overflow-y: auto;
}
</style>