<template>
  <div class="content-container">
    <headline label="ViteX Trading"/>
    <div class="content">
      <p class="description">Download statistics on trading as mining on ViteX by address as .csv file.</p>
      <v-text-field name="Vite Address" label="VITE Address" :onSubmit="onSubmit" :onChange="((inputValue) => this.form.address = inputValue.target.value)"/>
      <v-button-download :onSubmit="onSubmit" :requestInProgress="requestInProgress"/>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import VTextField from "../components/VTextField.vue";
import VButtonDownload from "../components/VButtonDownload.vue";
import Headline from "../components/Headline.vue";
export default {
  name: "Trading",
  components: {
    VTextField,
    VButtonDownload,
    Headline
  },
  data: () => ({
    form: {
      address: "",
    },
    requestInProgress: false,
  }),
  methods: {
    onSubmit: async function () {
      if (this.requestInProgress) return;
      if (this.form.address == "") {
        this.$vToastify.error("VITE address needed");
        return;
      }
      const infoToast = this.$vToastify.info("Generating csv");
      this.requestInProgress = true;
      try {
        const viteAddress = this.form.address;
        var params;
        params = {
          viteAddress: viteAddress,
        };

        console.log(params);
        const response = await axios.post(
          process.env.VUE_APP_API_URL + "mining/trading/",
          params
        );

        console.log(response);

        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", "trading_" + viteAddress.trim() + ".csv"); //or any other extension
        document.body.appendChild(link);
        link.click();
        this.$vToastify.removeToast(infoToast);
        this.$vToastify.success("CSV successfully generated");
      } catch (error) {
        console.log("error:", error.response.data);
        var errorMsg = "Something went wrong..."
        if (error.response.data) {
          const value = Object.values(error.response.data)[0]
          errorMsg = value;
        }
        this.$vToastify.removeToast(infoToast);
        this.$vToastify.error(errorMsg);
      } finally {
        this.requestInProgress = false;
      }
    },
  },
};
</script>