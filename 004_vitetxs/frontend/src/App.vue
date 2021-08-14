<template>
  <div class="main">
    <Menu />
    <router-view />
  </div>
</template>

<script>
import Menu from "./components/Menu.vue";
export default {
  components: {
    Menu,
  },
};
</script>
<style>
@import './global.css';

.main {
  width: 100%;
  min-height: 100%;
  display: flex;
  background: var(--blue-dark);
  background: linear-gradient(90deg, var(--blue-dark) 0%, var(--blue-dark) 15%, var(--blue-lightest) 100%);
}

@media (max-width: 1100px) {
  .main {
    flex-direction: column;
  }
}

</style>