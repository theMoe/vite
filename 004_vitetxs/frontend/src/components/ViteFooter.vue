<template>
  <div class="v-footer-container">
    <div class="v-footer-navigation">
      <el-button v-for="link in links" :key="link" type="text" disabled>
        {{ link }}
      </el-button>
    </div>
    <div class="v-copyright">
      Moe © {{ new Date().getFullYear() }}
    </div>
  </div>
</template>
<script>
export default {
  name: "ViteFooter",
  data: () => ({
    links: ["HOME", "ABOUT US", "TEAM", "CONTACT US"],
  }),
};
</script>