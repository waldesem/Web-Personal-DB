import { defineStore } from 'pinia';
import { io } from 'socket.io-client';


export const soketStore = defineStore('soketStore', () => {

  const chatBot = io()
    
  return { 
    chatBot, 
  }
});