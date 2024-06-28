import { createApp } from "vue";
import { router } from "@/router";
import App from "@/App.vue";

import "bootswatch/dist/journal/bootstrap.css";
import "bootstrap/dist/js/bootstrap.min.js";

createApp(App).use(router).mount("#app");
