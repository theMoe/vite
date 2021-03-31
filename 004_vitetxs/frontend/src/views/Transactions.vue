<template>
  <div class="content-container">
    <headline label="Transactions"/>
    <div class="content">
      <p class="description">Download VITE transactions by address as .csv file. It includes only transactions visible on the VITE address limited to the last 100k transactions. <b>Depending on the amount of transactions the process can take up to 30 minutes.</b></p>
      <v-text-field name="Vite Address" label="VITE Address [required]" :onSubmit="onSubmit" :onChange="((inputValue) => this.form.address = inputValue.target.value)"/>
      <v-multi-select
        label="Filter transactions" 
        tagplaceholder="Add this as new VITE address"
        placeholder="Search or add a VITE address" 
        name="Multiselect"
        :options="this.multiselectOptions"
        :multiple="true" 
        :taggable="true"
        :onChange="((inputValue) => updateFilter(inputValue))"
      />
      <v-date-picker label="From Date" :onSelect="((date) => updateDate(date, 'date1'))"  name="date1"/>
      <v-date-picker label="To Date" :onSelect="((date) => updateDate(date, 'date2'))" name="date2"/>
      <v-button-download :onSubmit="onSubmit" :requestInProgress="requestInProgress"/>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import dayjs from "dayjs";
import VDatePicker from "../components/VDatePicker.vue";
import VTextField from "../components/VTextField.vue";
import VButtonDownload from "../components/VButtonDownload.vue";
import VMultiSelect from "../components/VMultiSelect.vue";
import Headline from "../components/Headline.vue";
export default {
  name: "Transactions",
  components: {
    VDatePicker,
    VTextField,
    VButtonDownload,
    VMultiSelect,
    Headline,
  },
  data: () => ({
    form: {
      address: "",
      senderAddress: [],
      date1: "",
      date2: "",
    },
    multiselectOptions: [
      {"name": "Full Node Daily Rewards", "viteAddress": "vite_86f729c9b7dda636e46b7ae738785be87f71390f532828ace9"}, 
      {"name": "Wallet Staking Rewards", "viteAddress": "vite_79f6168f60d19dbf74c9f180264a14a47675f2840696873ff7"}, 
      {"name": "Vote Rewards - SwissVite.org", "viteAddress": "vite_99bf4a247462870dd2f777ff3fc16b0938ab6a38e7129565b2"},
    ],
    requestInProgress: false,
  }),
  methods: {
    updateFilter(value) {
      this.form.senderAddress = value.map(v => v.viteAddress);
      console.log(this.form.senderAddress);
    },
    updateDate(value, property) {
      this.form[property] = dayjs(value).format("YYYY-MM-DDT[00:00:00Z]");
      console.log(value);
    },
    onSubmit: async function () {
      console.log(this.form.senderAddress)
      if (this.requestInProgress) return;
      if (this.form.address == "") {
        this.$vToastify.error("VITE address needed");
        return;
      }
      const infoToast = this.$vToastify.info("Generating csv");
      this.requestInProgress = true;
      try {
        const viteAddress = this.form.address;
        const viteAddressSender = this.form.senderAddress;
        var params;
        var fromDate;
        var toDate;
        fromDate = dayjs(new Date("1900-01-01T00:00:00Z")).format("YYYY-MM-DDT[00:00:00Z]"); // '1900-01-01'; // new Date(Date.UTC(0, 0, 0, 0, 0, 0));
        toDate = dayjs(new Date("1900-01-01T00:00:00Z")).format("YYYY-MM-DDT[00:00:00Z]"); // '1900-01-01'; // new Date(Date.UTC(0, 0, 0, 0, 0, 0));
        if ((this.form.date1 != null && this.form.date2 != null) && (this.form.date1 != '' && this.form.date2 != '')) {
          fromDate = this.form.date1;
          toDate = this.form.date2;
        }

        params = {
          transactionsPerRequest: 1000,
          pageMax: 100,
          fromDate: fromDate,
          toDate: toDate,
          viteAddress: viteAddress,
          viteAddressSender: viteAddressSender,
        };

        console.log(params);
        const response = await axios.post(
          process.env.VUE_APP_API_URL + "transactions/",
          params
        );

        console.log(response);

        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", "transactions_" + viteAddress.trim() + ".csv"); //or any other extension
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