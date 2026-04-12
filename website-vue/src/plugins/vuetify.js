// src/plugins/vuetify.js
import { createVuetify } from 'vuetify';
import 'vuetify/styles'; // 引入樣式
import * as components from 'vuetify/components'; // 導入 Vuetify 組件
import * as directives from 'vuetify/directives'; // 導入 Vuetify 指令

const vuetify = createVuetify({
  components,
  directives,
});

export default vuetify;
