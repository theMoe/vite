<template>
  <div class="content-container">
    <headline label="ViteX Orders"/>
    <div class="content">
      Coming soon...
      <v-text-field label="" style="display: none;"/>
    </div>
  </div>
</template>
<script>
import Headline from "../components/Headline.vue";
import VTextField from "../components/VTextField.vue";
export default {
  name: "ExchangeOrders",
  components: {
    Headline,
    VTextField
  }
};
</script>