import { createApp } from "vue";
import { router } from "@/router";
import App from "@/App.vue";

import "bootstrap/dist/js/bootstrap.min.js";
import "bootstrap/dist/css/bootstrap.min.css";

createApp(App).use(router).mount("#app");
