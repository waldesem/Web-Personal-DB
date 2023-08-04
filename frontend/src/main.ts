import { createApp } from 'vue'
import router from './router/router'
import { createPinia } from 'pinia';
import App from './App.vue'

import "bootswatch/dist/journal/bootstrap.css";
import "bootstrap/dist/js/bootstrap.min.js";
import 'bootstrap-icons/font/bootstrap-icons.css'

createApp(App).use(router).use(createPinia()).mount('#app')
