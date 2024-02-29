<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { authStore } from "@store/auth";
import { server } from "@utilities/utils";
import { Message } from "@/interfaces/interface";

const MessagesToast = defineAsyncComponent(
  () => import("./MessagesToast.vue")
);

const storeAuth = authStore();

const messageData = ref({
  isStarted: false,
  messages: Array<Message>(),
  hasPrev: false,
  hasNext: false,
  currentPage: 1,

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

  updateCount: function () {
    if (!this.isStarted) {
      this.isStarted = true;
      setInterval(this.updateMessages, 1000000);
    }
  },
});

messageData.value.updateCount();
</script>

<template>
  <li class="nav-item dropdown">
    <a
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
    <div class="dropdown-menu">
      <MessagesToast :messages="messageData.messages"/>
      <div class="col text-end">
        <p>
          <a href="#" class="link-danger" @click="messageData.deleteMessage()">
            Удалить сообщения
          </a>
        </p>
      </div>
      <div class="py-2">
        <table class="table table-responsive align-middle">
          <thead>
            <tr>
              <th width="20%">Дата</th>
              <th>Сообщение</th>
            </tr>
          </thead>
          <tbody v-if="messageData.messages.length">
            <tr v-for="message, index in messageData.messages" :key="index">
              <td width="30%">{{ message["created"] }}</td>
              <td>{{ message["message"] }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </li>
</template>

<style scoped>
.dropdown {
  max-height: 75vh;
  overflow-y: auto;
}
</style>