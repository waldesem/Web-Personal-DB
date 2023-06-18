import { createApp } from 'vue'

import "bootswatch/dist/journal/bootstrap.css";
import "bootstrap/dist/js/bootstrap.min.js";

import App from './App.vue'
import router from './router';

createApp(App).use(router).mount('#app');