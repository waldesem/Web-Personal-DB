import { defineStore } from 'pinia';
import { ref } from 'vue';
import { io } from 'socket.io-client';
import { server } from '@share/utilities';

export const socketStore = defineStore('socketStore', () => {

  const socket = io(server);

  const chatDialog = ref<Array<Object>>([]);

  socket.on("connect", () => {
    if (socket.connected) {
      chatDialog.value.push({'chatBot': 'Добрый день! Чем я могу помочь?'});
    }
  });

  socket.on("disconnect", () => {
    chatDialog.value.push({'chatBot': 'До скорой встречи!'});
  });
  
  socket.on("incoming", (args) => {
    chatDialog.value.push(args);
  });
  
  socket.on("error", (args) => {
    chatDialog.value.push({'chatBot': args});
  });
  
  return {
    socket,
    chatDialog
  }
})
