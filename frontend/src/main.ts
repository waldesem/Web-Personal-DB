import { createApp } from "vue";
import { router } from "@/router";
import App from "@/App.vue";

// import "bootswatch/dist/journal/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.min.js";
import "bootstrap/dist/css/bootstrap.min.css";

createApp(App).use(router).mount("#app");
