import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import "bootswatch/dist/journal/bootstrap.css";
import "bootstrap/dist/js/bootstrap.min.js";
import 'bootstrap-icons/font/bootstrap-icons.css'

createApp(App).use(router).mount('#app')
