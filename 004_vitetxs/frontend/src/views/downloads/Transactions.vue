<template>
  <div class="download-card">
    <h3>Transactions</h3>
    <div class="content">
      <p class="description">Download VITE transactions by address as .csv file. It includes only transactions visible on the VITE address limited to the last 100k transactions. <br/><b>Depending on the amount of transactions the process can take up to 30 minutes.</b></p>
      <ViteInput name="Vite Address" label="VITE Address" required="true" :onChange="(inputValue) => (this.viteAddress = inputValue.target.value)" :onSubmit="getDataFromApi"/>
      <v-date-picker label="From Date" name="fromDate" :onSelect="(date) => (updateDate(date, 'fromDate'))" :onSubmit="getDataFromApi"/>
      <v-date-picker label="To Date" name="toDate" :onSelect="(date) => (updateDate(date, 'toDate'))" :onSubmit="getDataFromApi"/>
      <v-multi-select objectOptions="true" label="Filter transactions" tagplaceholder="Add this as new VITE address" placeholder="Search or add a VITE address" :multiple="true" :taggable="false" :options="multiselectOptions" :onChange="(inputValue) => (this.form.viteAddressSender = inputValue.map((address) => (address.viteAddress)))"/>
      <download-button :onSubmit="getDataFromApi" :requestInProgress="this.$store.state.transactions.loading.downloadLoading"/>
    </div>
    <v-snackbar
      v-model="snackbar"
      class="exception-snack"
      :timeout="7500"
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
import dayjs from "dayjs";
import ViteInput from "../../components/ViteInput.vue";
import VMultiSelect from "../../components/VMultiSelect.vue";
import VDatePicker from "../../components/VDatePicker.vue";
import DownloadButton from "../../components/DownloadButton.vue";
export default {
    components: {
        ViteInput,
        VMultiSelect,
        VDatePicker,
        DownloadButton
    },
  data: () => ({
    viteAddress: "",
    snackbar: false,
    form: {
      viteAddressSender: [],
      fromDate: "",
      toDate: "",
    },
    multiselectOptions: [
      {"name": "Full Node Daily Rewards", "viteAddress": "vite_1737bb7abc4883cc2f415a804f80274d3a725a68a5bee5bad3"},
      {"name": "Full Node Daily Rewards - OLD", "viteAddress": "vite_86f729c9b7dda636e46b7ae738785be87f71390f532828ace9"}, 
      {"name": "Wallet Staking Rewards", "viteAddress": "vite_79f6168f60d19dbf74c9f180264a14a47675f2840696873ff7"}, 
      {"name": "Vote Rewards - SwissVite.org", "viteAddress": "vite_99bf4a247462870dd2f777ff3fc16b0938ab6a38e7129565b2"},
    ],
  }),
  methods: {
    updateDate(value, property) {
      this.form[property] = dayjs(value).format("YYYY-MM-DD");
    },
    async getDataFromApi() {
      await this.$store.dispatch("transactions/getStatistics", {viteAddress: this.viteAddress, params: this.form});
      this.snackbar = this.$store.state.transactions.error;
    }
  }
}
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