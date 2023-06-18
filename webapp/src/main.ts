import { createApp } from 'vue'

import "bootswatch/dist/journal/bootstrap.css";
import "bootstrap/dist/js/bootstrap.min.js";

import App from './App.vue'
import router from './router';

const appUrl = 'http://localhost:5000';

export default appUrl;

createApp(App).use(router).mount('#app');