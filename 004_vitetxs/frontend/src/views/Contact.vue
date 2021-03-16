<template>
  <div class="content-container">
    <headline label="Contact"/>
    <div class="content home">
        <h5 class="contact-headline">Any feedback and feature ideas?</h5>
        <p id="contact">Contact us!</p>
        <div class="link-container contact">
          <div class="link">
            <p>Twitter</p>
            <v-link-button label="@VITEtools" href="https://twitter.com/VITEtools"/>
          </div>
          <div class="link">
            <p>GitHub</p>
            <v-link-button label="VITE tools" href="https://github.com/theMoe/vite/tree/main/004_vitetxs"/>
          </div>
        </div>
        <v-text-field label="" style="display: none;"/>        
    </div>
  </div>
</template>
<script>
import VTextField from "../components/VTextField.vue";
import VLinkButton from "../components/VLinkButton.vue";
import Headline from "../components/Headline.vue";
export default {
  name: "Contact",
  components: {
    Headline,
    VLinkButton,
    VTextField
  }
};
</script>