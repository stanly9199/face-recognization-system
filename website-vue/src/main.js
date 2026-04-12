
// src/main.js
import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // 確保正確導入
import axios from 'axios'; // 引入 Axios
import VueAxios from 'vue-axios'; // 引入 VueAxios 以便在 Vue 中使用

const app = createApp(App);

// 使用 router 和 axios
app.use(router);
app.use(VueAxios, axios); // 註冊 Axios 插件

app.mount('#app');

//export const BASE_URL = 'http://192.168.10.10:3000';
// export const BASE_URL = 'http://localhost:3000';
export const BASE_URL = 'https://lab305.ngrok.pro/api';
export const IMAGE_URL = `https://lab305.ngrok.pro/image`