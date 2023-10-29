<script setup lang="ts">
import { ref } from 'vue';
import { authStore } from '@/store/token';
import { server } from '@share/utilities';

const storeAuth = authStore();

const chatDialog = ref<Array<Object>>([]);
chatDialog.value.push({'chatBot': 'Добро пожаловать в чат!'});
const textInput  = ref('');

function clearChat() {
  chatDialog.value = [];
  chatDialog.value.push({'chatBot': 'Добро пожаловать в чат!'});
};

async function updateChat() {
  chatDialog.value.push({'Вы': textInput.value});
  try {
    const response = await storeAuth.axiosInstance.post(
      `${server}/chat`, {
        'data': textInput.value
      }
    );
    chatDialog.value.push(response.data);
  
  } catch (error) {
  chatDialog.value.push({'chatBot': error});
  }
  textInput.value = '';

  const chatcontent = document.getElementById('chatcontent');
  if (chatcontent) {
    chatcontent.scrollTop = chatcontent.scrollHeight;
  }
};

</script>

<template>
  <div>
    <a class="chatbot-button dropdown-toggle" role="button"  
      data-bs-toggle="dropdown" data-bs-auto-close="false">
      <i class="bi bi-chat-dots-fill fs-1"></i>
    </a>
    <div class="dropdown-menu" id="chatbot">
      <p class="dropdown-header text-center fs-5">StaffSecBot</p>
      <hr class="dropdown-divider">
      <div id="chatcontent">
        <div v-for="dialog, index in chatDialog" :key="index" 
            :class="`${Object.keys(dialog)[0] === 'chatBot' ? 'px-3' : 'px-5'} py-2`">
          <div :class="`p-3 bg-${Object.keys(dialog)[0] !== 'chatBot' ? 'danger' : 'success'} bg-opacity-75 border rounded text-wrap text-light`">
            {{ `${Object.keys(dialog)[0]}: ${Object.values(dialog)[0]}` }}
          </div>
        </div>
      </div>
      <div class="py-3">
        <form @submit.prevent="updateChat" class="form form-check" role="form">
          <div class="row">
            <div class="col-md-9">
              <input class="form-control" id="chat" name="chat" required v-model="textInput">
            </div>
            <div class="col-md-1">
              <button class="btn btn-outline-primary" title="Отправить" type="submit">
                <i class="bi bi-send"></i>
              </button>
            </div>
            <div class="col-md-1">
              <button class="btn btn-outline-secondary btn-lg" @click="clearChat" type="button" title="Очистить">
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
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    cursor: pointer;
    }
    
    .chatbot-button::after {
        display: none;
    }
    </style>