<template>
  <div class="content-container">
    <headline label="ViteX Orders"/>
    <div class="content vitex">
      <p class="description">Download ViteX order history by address as .csv file.</p>
      <v-text-field name="Vite Address" label="VITE Address [required]" :onSubmit="onSubmit" :onChange="((inputValue) => this.form.address = inputValue.target.value)"/>
      <v-date-picker label="From Date" :onSelect="((date) => updateDate(date, 'date1'))"  name="date1"/>
      <v-date-picker label="To Date" :onSelect="((date) => updateDate(date, 'date2'))" name="date2"/>
      <div class="form-element button-container filter-button">
        <div class="btn open-modal" @click="openModal">Filter options</div>
      </div>
      <v-button-download :onSubmit="onSubmit" :requestInProgress="requestInProgress"/>
      <div class="modal" id="filter-modal">
        <div class="modal-content">
          <div class="btn close-modal" @click="closeModal">&times;</div>
          <h3>Filter Orders</h3>
          <v-multi-select
            label="Buy/Sell" 
            tagplaceholder="Add this as new VITE address"
            placeholder="Filter to only sell or buy orders" 
            name="MultiselectBuySell"
            :options="this.multiselectOptionsBuySell"
            :multiple="false" 
            :taggable="false"
            :searchable="false"
            :onChange="((inputValue) => updateFilterSellBuy(inputValue))"
          />
          <v-multi-select
            label="Order Status" 
            tagplaceholder="Add this as new VITE address"
            placeholder="Filter to orders with specific status" 
            name="MultiselectStatus"
            :options="this.multiselectOptionsStatus"
            :multiple="false" 
            :taggable="false"
            :searchable="true"
            :onChange="((inputValue) => updateFilterStatus(inputValue))"
          />
          <v-multi-select
            label="Trade Pair" 
            tagplaceholder="Add this as new VITE address"
            placeholder="Filter to specific trade pair orders" 
            name="MultiselectSymbol"
            :options="this.multiselectOptionsSymbol"
            :multiple="false" 
            :taggable="false"
            :searchable="true"
            :onChange="((inputValue) => updateFilterSymbol(inputValue))"
          />
          <v-multi-select
            label="Trade Token" 
            tagplaceholder="Add this as new VITE address"
            placeholder="Filter to specific traded token orders" 
            name="MultiselectTradeToken"
            :options="this.multiselectOptionsTradeToken"
            :multiple="false" 
            :taggable="false"
            :searchable="true"
            :onChange="((inputValue) => updateFilterTradeToken(inputValue))"
          />
          <v-multi-select
            label="Quote Token" 
            tagplaceholder="Add this as new VITE address"
            placeholder="Filter to specific quoted token orders" 
            name="MultiselectQuoteToken"
            :options="this.multiselectOptionsQuoteToken"
            :multiple="false" 
            :taggable="false"
            :searchable="true"
            :onChange="((inputValue) => updateFilterQuoteToken(inputValue))"
          />
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import dayjs from "dayjs";
import Headline from "../components/Headline.vue";
import VDatePicker from "../components/VDatePicker.vue";
import VTextField from "../components/VTextField.vue";
import VMultiSelect from "../components/VMultiSelect.vue";
import VButtonDownload from "../components/VButtonDownload.vue";
export default {
  name: "ExchangeOrders",
  components: {
    Headline,
    VDatePicker,
    VTextField,
    VButtonDownload,
    VMultiSelect,
  },
  data: () => ({
    form: {
      address: "",
      date1: "",
      date2: "",
      sellBuy: null,
      symbol: null,
      tradeToken: null,
      quoteToken: null,
      orderStatus: null,
    },
    multiselectOptionsBuySell: [
      {"name": "Buy", "value": 0}, 
      {"name": "Sell", "value": 1}, 
    ],
    multiselectOptionsStatus: [
      {"name": "Unkown", "value": 0}, 
      {"name": "Pending", "value": 1},
      {"name": "Received", "value": 2},
      {"name": "Open", "value": 3},
      {"name": "Filled", "value": 4},
      {"name": "Partially Filled", "value": 5},
      {"name": "Pending Cancel", "value": 6},
      {"name": "Cancelled", "value": 7},
      {"name": "Partially", "value": 8},
      {"name": "Failed", "value": 9},
      {"name": "Expired", "value": 10}, 
    ],
    multiselectOptionsSymbol: [],
    multiselectOptionsTradeToken: [],
    multiselectOptionsQuoteToken: [],
    requestInProgress: false,
  }),
  mounted: () => {
    const modal = document.getElementById("filter-modal");
    window.onclick = function(event) {
      if (event.target == modal) {
        modal.style.display = "none";
      }
    }
  },
  created: async function () {
    try {
      const response = await axios.post(
        process.env.VUE_APP_API_URL + "markets/"
      );

      if ("data" in response.data) {
        if ("symbols" in response.data.data) {
          response.data.data.symbols.forEach(element => {
            this.multiselectOptionsSymbol.push({"name": element, "value": element});
          });
        }
        if ("tradeTokens" in response.data.data) {
          response.data.data.tradeTokens.forEach(element => {
            this.multiselectOptionsTradeToken.push({"name": element, "value": element});
          });
        }
        if ("quoteTokens" in response.data.data) {
          response.data.data.quoteTokens.forEach(element => {
            this.multiselectOptionsQuoteToken.push({"name": element, "value": element});
          });
        }
      } else {
        console.log("data error");
      }
    } catch (error) {
      console.log("error:", error.response.data);
    }
  },
  methods: {
    openModal() {
      const modal = document.getElementById("filter-modal");
      modal.style.display = "block";
    },
    closeModal() {
      const modal = document.getElementById("filter-modal");
      modal.style.display = "none";
    },
    updateDate(value, property) {
      this.form[property] = dayjs(value).format("YYYY-MM-DDT[00:00:00Z]");
    },
    updateFilterSellBuy(value) {
      if (value == null) {
        this.form.sellBuy = null
      } else {
        this.form.sellBuy = value.value;
      }
    },
    updateFilterStatus(value) {
      if (value == null) {
        this.form.orderStatus = null
      } else {
        this.form.orderStatus = value.value;
      }
    },
    updateFilterSymbol(value) {
      if (value == null) {
        this.form.symbol = null
      } else {
        this.form.symbol = value.value;
      }
    },
    updateFilterTradeToken(value) {
      if (value == null) {
        this.form.tradeToken = null
      } else {
        this.form.tradeToken = value.value;
      }
    },
    updateFilterQuoteToken(value) {
      if (value == null) {
        this.form.quoteToken = null
      } else {
        this.form.quoteToken = value.value;
      }
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
        const sellBuy = this.form.sellBuy;
        const orderStatus = this.form.orderStatus
        const symbol = this.form.symbol;
        const tradeToken = this.form.tradeToken;
        const quoteToken = this.form.quoteToken;
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
          viteAddress: viteAddress,
          fromDate: fromDate,
          toDate: toDate,
          limit: 100,
          sellBuy: sellBuy,
          orderStatus: orderStatus,
          symbol: symbol,
          tradeToken: tradeToken,
          quoteToken: quoteToken,
        };

        const response = await axios.post(
          process.env.VUE_APP_API_URL + "orders/",
          params
        );

        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", "orders_" + viteAddress.trim() + ".csv"); //or any other extension
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