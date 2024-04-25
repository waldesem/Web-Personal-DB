<script setup lang="ts">
import { onBeforeMount, ref } from "vue";
import { axiosAuth } from "@/auth";
import { server, timeSince } from "@/utilities";
import { Message } from "@/interfaces";

onBeforeMount(() => {
  updateMessages();
});

const messageData = ref({
  isStarted: false,
  messages: Array<Message>(),
});

async function updateMessages(): Promise<void> {
  try {
    const response = await axiosAuth.get(
      `${server}/messages`
    );
    const { messages } = response.data;
    messageData.value.messages = messages;
  } catch (error) {
    console.error(error);
  }
  if (!messageData.value.isStarted) {
    messageData.value.isStarted = true;
    setInterval(updateMessages, 1000000);
  }
};

async function deleteMessage(event: Event, iD: number = 0): Promise<void> {
  event.preventDefault();
  try {
    const response = await axiosAuth.delete(
      `${server}/messages/${iD}`,
    );
    console.log(response.status);
    updateMessages();
  } catch (error) {
    console.error(error);
  }
}
</script>

<template>
  <a 
    href="#offcanvasMessage"
    role="button"
    data-bs-toggle="offcanvas"
  >
  <i class="fs-3" 
    :class="`${messageData.messages.length ? 'bi bi-bell-fill' : 'bi bi-bell'}`"
  >
  </i>
    <span
      v-if="messageData.messages.length"
      class="position-absolute translate-middle badge rounded-pill text-bg-success"
    >
      {{ messageData.messages.length }}
    </span>
  </a>
  <div class="offcanvas offcanvas-end" data-bs-scroll="true" id="offcanvasMessage">
    <div class="offcanvas-body">
      <div class="d-flex justify-content-between mb-3">
        <button 
          class="btn btn-link"
          title="Обновить сообщения"
          @click="updateMessages"
        >
          <i class="bi bi-arrow-clockwise"></i>
        </button>
        <button 
          class="btn btn-link"
          title="Удалить все сообщения"
          @click="deleteMessage"
        >
          <i class="bi bi-trash"></i>
        </button>
      </div>
      <div 
        v-for="message, index in messageData.messages" :key="index"
        class="card mb-3" 
      >
        <div class="card-header">
          <small class="d-flex justify-content-between">
              {{ timeSince(message["created"]) }}
            <button 
              type="button" 
              class="btn-close btn-sm" 
              @click="deleteMessage($event, parseInt(message['id']))"
            >
            </button>
          </small>
        </div>
        <small class="card-body text-break text-start">
          {{ message["message"] }}
        </small>
      </div>
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