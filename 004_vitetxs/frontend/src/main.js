import '@babel/polyfill'
import 'mutationobserver-shim'
import Vue from 'vue'
import './plugins/axios'
import App from './App.vue'
import './plugins/dayjs'
import './plugins/element.js'
import router from './router'
import VueToastify from "vue-toastify";
Vue.config.productionTip = false

Vue.use(VueToastify);

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
