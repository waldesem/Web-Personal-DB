<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { authStore } from "@store/token";
import { server } from "@utilities/utils";

const PageSwitcher = defineAsyncComponent(
  () => import("@components/layouts/PageSwitcher.vue")
);
const MessagesToast = defineAsyncComponent(
  () => import("@components/layouts/MessagesToast.vue")
);

const storeAuth = authStore();

interface Message {
  title: string
  message: string
  status: string
  created: string
}

onBeforeMount(async () => {
  await messageData.value.updateMessages("all");
});

const messageData = ref({
  isStarted: false,
  messages: Array<Message>(),
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
    Сообщения
    <span
      class="position-absolute translate-middle badge rounded-pill text-bg-success"
    >
      {{ messageData.messages.length }}
    </span>
    <MessagesToast :messages="messageData.messages"/>
    <div>
      <div class="row justify-content-between">
        <div class="col">
          <p>
            <a
              href="#"
              class="link-info"
              @click="messageData.updateMessages('read')"
            >
              Отметить все прочитанными
            </a>
          </p>
        </div>
        <div class="col text-end">
          <p>
            <a href="#" class="link-danger" @click="messageData.deleteMessage()">
              Удалить все сообщения
            </a>
          </p>
        </div>
      </div>
      <div class="py-2">
        <table class="table table-responsive align-middle">
          <thead>
            <tr>
              <th width="5%">#</th>
              <th width="15%">Категория</th>
              <th width="15%">Тема</th>
              <th>Сообщение</th>
              <th width="15%">Статус</th>
              <th width="10%">Дата</th>
            </tr>
          </thead>
          <tbody v-if="messageData.messages.length">
            <tr v-for="message, index in messageData.messages" :key="index">
              <td width="15%">{{ message["title"] }}</td>
              <td>{{ message["message"] }}</td>
              <td width="15%">{{ message["status"] }}</td>
              <td width="15%">{{ message["created"] }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <PageSwitcher
        :has_prev="messageData.hasPrev"
        :has_next="messageData.hasNext"
        :switchPrev="messageData.currentPage - 1"
        :switchNext="messageData.currentPage + 1"
        :switchPage="messageData.updateMessages"
        :option="'all'"
      />
    </div>
  </li>
</template>
@/utilities/token