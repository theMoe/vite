<template>
  <div class="download-card">
    <h3>ViteX Orders</h3>
    <div class="content">
      <p class="description">Download ViteX order history by address as .csv file.</p>
      <ViteInput name="Vite Address" label="VITE Address" required="true" :onChange="(inputValue) => (this.viteAddress = inputValue.target.value)" :onSubmit="getDataFromApi"/>
      <v-date-picker label="From Date" name="fromDate" :onSelect="(date) => (updateDate(date, 'fromDate'))" :onSubmit="getDataFromApi"/>
      <v-date-picker label="To Date" name="toDate" :onSelect="(date) => (updateDate(date, 'toDate'))" :onSubmit="getDataFromApi"/>
      <!-- Filter options -->
      <fieldset class="filter-options">
        <legend>Filter options</legend>
        <v-multi-select label="Buy/Sell" placeholder="Filter to only sell or buy orders" :options="this.multiselectOptionsBuySell" :multiple="false" :taggable="false" :searchable="false" :onChange="(inputValue) => (this.form.sellBuy = inputValue)"/>
        <v-multi-select label="Order Status" placeholder="Filter to orders with specific status" :options="this.multiselectOptionsStatus" :multiple="false" :taggable="false" :searchable="true" :onChange="(inputValue) => (this.form.orderStatus = inputValue)"/>
        <v-multi-select label="Trade Pair" placeholder="Filter to specific trade pair orders" :options="this.multiselectOptionsTradePair" :multiple="false" :taggable="false" :searchable="true" :onChange="(inputValue) => (this.form.tradePair = inputValue)"/>
        <v-multi-select label="Trade Token" placeholder="Filter to specific traded token orders" :options="this.multiselectOptionsTradeToken" :multiple="false" :taggable="false" :searchable="true" :onChange="(inputValue) => (this.form.tradeToken = inputValue)"/>
        <v-multi-select label="Quote Token" placeholder="Filter to specific quoted token orders" :options="this.multiselectOptionsQuoteToken" :multiple="false" :taggable="false" :searchable="true" :onChange="(inputValue) => (this.form.quoteToken = inputValue)"/>
      </fieldset>
      <download-button :onSubmit="getDataFromApi" :requestInProgress="this.$store.state.exchangeOrders.loading"/>
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
    form: {
      fromDate: "",
      toDate: "",
      sellBuy: null,
      tradePair: null,
      tradeToken: null,
      quoteToken: null,
      orderStatus: null,
    },
    multiselectOptionsBuySell: ["Buy", "Sell"],
    multiselectOptionsStatus: ["Unknown", "Pending", "Received", "Open", "Filled", "Partially Filled", "Pending Cancel", "Cancelled", "Partially", "Failed", "Expired"],
    multiselectOptionsTradePair: [],
    multiselectOptionsTradeToken: [],
    multiselectOptionsQuoteToken: [],
    snackbar: false,
  }),
  methods: {
    async getMultiselectData() {
      const multiselectData = await this.$store.dispatch("exchangeOrders/getMultiselectData");
      this.multiselectOptionsTradePair = multiselectData.tradePairs;
      this.multiselectOptionsTradeToken = multiselectData.tradeTokens;
      this.multiselectOptionsQuoteToken = multiselectData.quoteTokens;
    },
    updateDate(value, property) {
      this.form[property] = dayjs(value).format("YYYY-MM-DD");
    },
    async getDataFromApi() {
      await this.$store.dispatch("exchangeOrders/getStatistics", {viteAddress: this.viteAddress, params: this.form});
      this.snackbar = this.$store.state.exchangeOrders.error;
    }
  },
  created() {
    this.getMultiselectData();
  },
  watch: {
    statisticInProgress(newValue) {
      this.inProgress = newValue;
    },
    statisticDownloadError(newValue) {
      this.errorMessage = newValue;
    },
  },

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

.filter-options {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  border-radius: 10px;
  border: 1px solid var(--blue);
  padding-top: 20px;
  margin: 20px 0;
}

.filter-options legend {
  font-size: 14pt;
  color: var(--blue);
}

.filter-options > * {
  flex-basis: 95%;
}

@media (max-width: 600px) {
  .download-card {
    padding: 20px 20px 40px;
  }
}
</style>