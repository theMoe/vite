<template>
  <a class="link-button" :href="href" target="_blank">{{label}}</a>
</template>
<script>
export default {
  props: ["label", "href"]
};
</script>