import { createApp } from "vue";
import { createPinia } from "pinia";
import { similarityScore } from "./utils/similarity";
import App from "./App.vue";
import router from "./router";

import "./assets/main.css";

const app = createApp(App);

const res = similarityScore("./assets/greenery/Greenery1.jpg", "");
console.log(res);

app.use(createPinia());
app.use(router);

app.mount("#app");
