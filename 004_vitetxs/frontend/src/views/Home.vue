<template>
  <div class="content-container">
    <headline label="VITE tools"/>
    <div class="content home">
      <p class="description">With VITE tools you can download several data e.g. transcations, mining
        data as .csv files. All data will be requested in real time from the VITE chain or from ViteX API.<br/></p>
      <h5 id="vite-community">VITE Community</h5>
      <div class="link-container">
        <v-link-button label="vite.org" href="https://www.vite.org"/>  
        <v-link-button label="exchange" href="https://x.vite.net"/>  
        <v-link-button label="vite scan" href="https://vitescan.io"/>  
        <v-link-button label="explorer" href="https://explorer.vite.net"/>
      </div>
      <div class="donation-container">
        <p class="vite-donation">Scan with VITE wallet and say thank you<br/></p>
        <p class="vite-donation address">vite_a47eae663ea3a90ffe9651e2855cc8c7fe90456104e281f3d1<br/></p>
        <div class="vite-qr-code">
          <img src="../assets/viteTxsDonationAddress.png" alt="vite_a47eae663ea3a90ffe9651e2855cc8c7fe90456104e281f3d1" height="80" width="80" />
        </div>
      </div>
      <v-text-field label="" style="display: none;"/>
    </div>
  </div>
</template>
<script>
import Headline from "../components/Headline.vue";
import VLinkButton from "../components/VLinkButton.vue";
import VTextField from "../components/VTextField.vue";
export default {
  name: "Home",
  components: {
    Headline,
    VLinkButton,
    VTextField
  }
};
</script>