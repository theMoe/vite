<template>
  <div class="download-card">
    <h3>Market Making</h3>
    <div class="content">
      <p class="description">Download details on market mining on ViteX by address as .csv file.</p>
      <ViteInput name="Vite Address" label="VITE Address" required="true" :onSubmit="getDataFromApi" :onChange="(inputValue) => (this.viteAddress = inputValue.target.value)"/>
      <download-button :onSubmit="getDataFromApi" :requestInProgress="this.$store.state.markets.loading"/>
    </div>
    <v-snackbar
      v-model="snackbar"
      :timeout="7500"
      class="exception-snack"
      top
    >
      Data could not be loaded.
      <template v-slot:action="{ attrs }">
        <v-btn
          color="blue"
          text
          v-bind="attrs"
          @click="snackbar = false"
        >
         <p class="close-button">x</p>
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import ViteInput from "../../components/ViteInput.vue";
import DownloadButton from "../../components/DownloadButton.vue";
export default {
  components: {
    ViteInput,
    DownloadButton,
  },
  data: () => ({
    viteAddress: "",
    inProgress: false,
    errorMessage: "",
    snackbar: false,
  }),
  methods: {
    async getDataFromApi() {
      await this.$store.dispatch("markets/getStatistics", this.viteAddress);
      this.snackbar = this.$store.state.markets.error;
    }
  },
  watch: {
    statisticInProgress(newValue) {
      this.inProgress = newValue;
    },
    statisticDownloadError(newValue) {
      this.errorMessage = newValue;
    },
  },
  computed: {
    statisticInProgress() {
      return this.$store.state.dividends.loading;
    },
    statisticDownloadError() {
      return this.$store.state.dividends.errorMessage;
    },
  },
};
</script>

<style scoped>
.download-card {
  padding: 30px 50px 50px;
  width: 100%;
}

.download-card h3 {
  width: 100%;
  margin: 0 0 40px;
  text-align: center;
  font-size: 32pt;
  font-weight: 400;
  color: var(--blue-dark)
}

.content {
  display: flex;
  flex-wrap: wrap;
  width: 100%;
}

.content > * {
  flex-basis: 100%;
}

.description {
  font-size: 13pt;
  line-height: 180%;
  margin: 0 0 50px;
}

@media (max-width: 600px) {
  .download-card {
    padding: 20px 20px 40px;
  }
}
</style>