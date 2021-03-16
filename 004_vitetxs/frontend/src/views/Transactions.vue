<template>
  <div class="content-container">
    <headline label="Transactions"/>
    <div class="content">
      <p class="description">Download VITE transactions by address as .csv file. It includes only transactions visible on the VITE address limited to the last 100k transactions.</p>
      <v-text-field name="Vite Address" label="VITE Address" :onSubmit="onSubmit" :onChange="((inputValue) => this.form.address = inputValue.target.value)"/>
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
import Headline from "../components/Headline.vue";
export default {
  name: "Transactions",
  components: {
    VDatePicker,
    VTextField,
    VButtonDownload,
    Headline,
  },
  data: () => ({
    form: {
      address: "",
      date1: "",
      date2: "",
    },
    requestInProgress: false,
  }),
  methods: {
    updateDate(value, property) {
      this.form[property] = dayjs(value).format("YYYY-MM-DDT[00:00:00Z]");
      console.log(value);
    },
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
          fromDate: fromDate, // dayjs(fromDate).toISOString(),
          toDate: toDate, // dayjs(toDate).toISOString(),
          viteAddress: viteAddress,
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
          //const [key, value] = Object.entries(error.response.data)[0]
          //console.log(key)
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