<template>
  <div class="download-card">
    <h3>ViteX Price History</h3>
    <div class="content">
      <p class="description">Download ViteX price history by trade pair as .csv file. Request is limited to max 1,500 results.</p>
      <v-multi-select label="Trade Pair" tagplaceholder="Add this as new VITE address" placeholder="Select trade pair" name="MultiselectSymbol" :options="this.multiselectOptionsTradePair" :multiple="false" :taggable="false" :searchable="true" :onChange="((inputValue) => (this.form.tradePair = inputValue))" required="true"/>
      <v-multi-select objectOptions="true" label="Filter interval" tagplaceholder="" placeholder="Search interval" name="MultiselectInterval" :options="this.multiselectOptionsInterval" :multiple="false" :taggable="false" :searchable="false" :onChange="((inputValue) => (this.form.interval = inputValue.value))" required="true"/>
      <v-date-picker label="From Date" name="fromDate" :onSelect="(date) => (updateDate(date, 'fromDate'))" :onSubmit="getDataFromApi"/>
      <v-date-picker label="To Date" name="toDate" :onSelect="(date) => (updateDate(date, 'toDate'))" :onSubmit="getDataFromApi"/>
      <download-button :onSubmit="getDataFromApi" :requestInProgress="this.$store.state.prices.loading"/>
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
import VMultiSelect from "../../components/VMultiSelect.vue";
import VDatePicker from "../../components/VDatePicker.vue";
import DownloadButton from "../../components/DownloadButton.vue";
export default {
    components: {
      VMultiSelect,
      VDatePicker,
      DownloadButton
    },
  data: () => ({
    form: {
      tradePair: "",
      interval: "",
      fromDate: "",
      toDate: "",
    },
    multiselectOptionsInterval: [
      {"name": "1 Minute", "value": "minute"}, 
      {"name": "30 Minutes", "value": "minute30"}, 
      {"name": "1 Hour", "value": "hour"},
      {"name": "6 Hours", "value": "hour6"},
      {"name": "12 Hours", "value": "hour12"},
      {"name": "1 Day", "value": "day"},
      {"name": "1 Week", "value": "week"},
    ],
    multiselectOptionsTradePair: [],
    snackbar: false
  }),
  methods: {
    async getMultiselectData() {
      const multiselectData = await this.$store.dispatch("exchangeOrders/getMultiselectData");
      this.multiselectOptionsTradePair = multiselectData.tradePairs;
    },
    updateDate(value, property) {
      this.form[property] = dayjs(value).format("YYYY-MM-DD");
    },
    async getDataFromApi() {
      this.$store.dispatch("prices/getStatistics", this.form);
      this.snackbar = this.$store.state.prices.error;
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

@media (max-width: 600px) {
  .download-card {
    padding: 20px 20px 40px;
  }
}
</style>