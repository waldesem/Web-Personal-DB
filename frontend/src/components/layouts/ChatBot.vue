<script setup lang="ts">

import { ref } from 'vue';
import { authStore } from '@/store/token';
import { server } from '@utilities/utils';

const storeAuth = authStore();

const chatBot = ref({
  dialog: <Array<Object>>[{'chatBot': 'Добро пожаловать в чат!'}],
  input: '',
  spinner: false,

  updateChat: async function () {
    this.spinner = true;
    this.dialog.push({'Вы': this.input});
    try {
      const response = await storeAuth.axiosInstance.post(
        `${server}/chat`, {
          'data': this.input
        }
      );
      this.dialog.push(response.data);
    
    } catch (error) {
    this.dialog.push({'chatBot': error});
    };
    this.input = '';
    this.scrollChat();
    this.spinner = false;
  },

  scrollChat: function(){
    const chatcontent = document.getElementById('chatcontent');
    if (chatcontent) {
      chatcontent.scrollTop = chatcontent.scrollHeight;
    }
  },

  clearChat: function () {
    this.dialog = [{'chatBot': 'Добро пожаловать в чат!'}];
  },
});

</script>

<template>
  <div class="d-print-none">
    <a class="chatbot-button dropdown-toggle" role="button"  
      data-bs-toggle="dropdown" data-bs-auto-close="false">
      <i class="bi bi-chat-dots-fill fs-1"></i>
    </a>
    <div class="dropdown-menu" id="chatbot">
      <p class="dropdown-header text-center fs-5">StaffSecBot</p>
      <hr class="dropdown-divider">
      <div id="chatcontent">
        <div v-for="dialog, index in chatBot.dialog" :key="index" 
            :class="`${Object.keys(dialog)[0] === 'chatBot' ? 'px-3' : 'px-5'} py-2`">
          <div :class="`p-3 bg-${Object.keys(dialog)[0] !== 'chatBot' ? 'danger' : 'success'} bg-opacity-75 border rounded text-wrap text-light`">
            {{ `${Object.keys(dialog)[0]}: ${Object.values(dialog)[0]}` }}
          </div>
        </div>
      </div>
      <div class="py-3">
        <form @submit.prevent="chatBot.updateChat" class="form form-check" role="form">
          <div class="row">
            <div class="col-md-9">
              <input class="form-control" id="chat" name="chat" 
                     required v-model="chatBot.input">
            </div>
            <div class="col-md-1">
              <button :disabled="chatBot.spinner" class="btn btn-outline-primary btn-sm" 
                       title="Отправить" type="submit">
                <i class="bi bi-send"></i>
                <span v-if="chatBot.spinner" class="spinner-grow spinner-grow-sm text-primary"></span>
                <span v-if="chatBot.spinner" class="visually-hidden" role="status">Отправка...</span>
              </button>
            </div>
            <div class="col-md-1">
              <button :disabled="chatBot.spinner" class="btn btn-outline-secondary btn-sm" 
                      @click="chatBot.clearChat" type="button" title="Очистить">
                <i class="bi bi-trash"></i>
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style>
  #chatbot{
    width: 640px;
    height: 640px;
  }

  #chatcontent
  { 
    width: 620px;
    height: 480px;
    overflow-y: auto;
  }

  .chatbot-button {
    position: fixed;
    bottom: 40px;
    right: 40px;
    z-index: 9999;
    border-radius: 50%;
    padding: 10px;
    cursor: pointer;
    }
    
    .chatbot-button::after {
        display: none;
    }
    </style>