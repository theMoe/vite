<template>
  <div class="main-card">
    <vite-app-bar-vue />
    <router-view />
  </div>
</template>

<script>
// import axios from "axios";
import ViteAppBarVue from "./ViteAppBar.vue";
export default {
  components: {
    ViteAppBarVue
  },
  name: "NewMain"
};
</script>