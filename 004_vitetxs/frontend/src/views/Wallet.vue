<template>
  <div class="content-container" id="wallet" data-app>
    <v-dialog
      v-model="dialog"
      persistent>
      <div class="modal-content">
        <h3>Please enter your VITE address</h3>
        <ViteInput name="Vite Address" label="VITE Address" required="true" :onSubmit="setViteAddress" :onChange="(inputValue) => (this.viteAddress = inputValue.target.value)"/>
        <div class="button-container"> 
          <button v-on:click="setViteAddress" class="submit">Submit</button>
        </div>
        <button v-on:click="dialog = false" class="close">X</button>
      </div>
      <v-snackbar
        v-model="errorSnackbar"
        :timeout="5000"
        color="#8f1007"
        top
      >
        Please enter a valid VITE Address.
        <template v-slot:action="{ attrs }">
          <v-btn
            color="blue"
            text
            v-bind="attrs"
            @click="errorSnackbar = false"
          >
          x
          </v-btn>
        </template>
      </v-snackbar>
    </v-dialog>
    <div v-if="!this.$store.state.globalViteAddress && !dialog" class="no-address">
      <div class="open-dialog-card card">
        <h2>Enter your VITE address to view this page.</h2>
        <button v-on:click="dialog = true" class="submit enter">Enter Address</button>
      </div>
    </div>
    <div v-else-if="!dialog" class="wallet-content">
      <div class="card overview-card">
        <div class="headline">
          <h2>Overview</h2>
        </div>
        <div v-if="!this.$store.state.wallet.loading.basicDataLoading" class="data-grid">
          <p class="category">Address:</p>
          <p class="value">{{viteAddress}} <span v-on:click="copyToClipboard(viteAddress)"><i class="fas fa-copy"/></span></p>
          <p class="category">VITE Balance:</p>
          <p class="value">{{this.$store.state.wallet.basicData.viteBalance || 0}} VITE</p>
          <p class="category">Staked VITE:</p>
          <p class="value">{{this.$store.state.wallet.basicData.stakedVite || 0}} VITE</p>
          <p class="category">Quota:</p>
          <p class="value">{{this.$store.state.wallet.basicData.quota || 0}} UT</p>
        </div>
        <div v-else class="loading">
          <v-progress-circular
              indeterminate
              color="#06254b"
              class="loading-spinner"
              :size="50"
            />
        </div>
        <div class="button-container">
          <v-btn
              @click="dialog = true"
              color="#06254b"
              dark
            >Change VITE Address <i class="fas fa-sync"/></v-btn>
        </div>
      </div>
      <div class="card wallet-token-card">
        <div class="headline">
          <h2>Tokens</h2>
        </div>
        <div class="subcard table-subcard">
          <div v-if="!this.$store.state.wallet.loading.tokenDataLoading" class="table-wrapper">
            <v-data-table :headers="this.$store.state.wallet.tokenListData.header" :items="this.$store.state.wallet.tokenListData.items" :items-per-page="5" :custom-sort="customSort" class="data-table wallet-token-table">
            </v-data-table>
          </div>
          <div v-else class="table-wrapper loading">
            <v-progress-circular
              indeterminate
              color="#e4e9ee"
              class="loading-spinner"
              :size="50"
            />
          </div>
        </div>
        <div v-if="!this.$store.state.wallet.loading.tokenDataLoading" class="subcard graph-subcard">
          <canvas id="token-graph"></canvas>
        </div>
        <div v-else class="subcard graph-subcard loading">
          <v-progress-circular
            indeterminate
            color="#e4e9ee"
            class="loading-spinner"
            :size="50"
        />
        </div>
      </div> 
      <div class="card node-card">
        <div class="overview-headline">
          <h2>Full Nodes</h2>
        </div>
        <div class="input-line">
          <p>choose a <span>cycle</span>:</p>
          <input v-model="cycle"/>
          <p class="info">(683-{{getCurrentCycle()}})</p>
          <div class="button-container">
            <v-btn
              @click="getListData"
              color="#06254b"
              dark
            >
              Change Cycle
              <i class="fas fa-sync"/>
            </v-btn>
          </div>
        </div>
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Search"
          single-line
          hide-details
          class="search"
        ></v-text-field>
        <div v-if="!this.$store.state.wallet.loading.nodeListLoading" class="table-wrapper">
          <v-data-table :headers="this.$store.state.wallet.nodeListData.header" :items="this.$store.state.wallet.nodeListData.items" :items-per-page="15" class="data-table node-table" multi-sort :search="search">
            <template v-slot:item.online_ratio="{ item }">
              <v-chip
                :color="getColorForRatio(item.online_ratio)"
                dark
                outlined
              >
                {{ item.online_ratio }}
              </v-chip>
            </template>
            <template v-slot:item.status="{ item }">
              <v-chip
                :color="getColorForStatus(item.status)"
                dark
                label
              >
                {{ item.status }}
              </v-chip>
            </template>
          </v-data-table>
        </div>
        <div v-else class="table-wrapper loading">
          <v-progress-circular
            indeterminate
            color="#06254b"
            class="loading-spinner"
            :size="50"
          />
        </div>
      </div>
      <div class="card transaction-card">
        <div class="overview-headline">
          <h2>Transactions</h2>
        </div>
        <div v-if="!this.$store.state.wallet.loading.transactionListLoading" class="table-wrapper">
          <v-data-table :headers="this.$store.state.wallet.transactionListData.header" :items="this.$store.state.wallet.transactionListData.items" :items-per-page="15" :custom-sort="customSort" class="data-table transaction-table" multi-sort>
            <template v-slot:item.created_at="{ item }">
              <span class="one-line-slot">{{ item.created_at }}</span>
            </template>
            <template v-slot:item.from_address_short="{ item }">
              <v-tooltip top>
                <template v-slot:activator="{ on, attrs }">
                  <span v-bind="attrs" v-on="on" class="one-line-slot">
                    {{item.from_address_short}}
                    <span v-on:click="copyToClipboard(item.from_address)" class="clickable-slot"><i class="fas fa-copy"/></span>
                  </span>
                </template>
                <span>{{item.from_address}}</span>
              </v-tooltip>
            </template>
            <template v-slot:item.to_address_short="{ item }">
              <v-tooltip top>
                <template v-slot:activator="{ on, attrs }">
                  <span v-bind="attrs" v-on="on" class="one-line-slot">
                    {{item.to_address_short}}
                    <span v-on:click="copyToClipboard(item.to_address)" class="clickable-slot"><i class="fas fa-copy"/></span>
                  </span>
                </template>
                <span>{{item.to_address}}</span>
              </v-tooltip>
            </template>
            <template v-slot:item.details="{ item }">
              <transaction-details :item="item"/>
            </template>
          </v-data-table>
        </div>
        <div v-else class="table-wrapper">
          <v-progress-circular
            indeterminate
            color="#06254b"
            class="loading-spinner"
            :size="50"
          />
        </div>
      </div>
      <v-snackbar
        v-model="snackbar"
        :timeout="2000"
        class="copy-snackbar"
      >
        Copied!
        <template v-slot:action="{ attrs }">
          <v-btn
            color="blue"
            text
            v-bind="attrs"
            @click="snackbar = false"
          >
          x
          </v-btn>
        </template>
      </v-snackbar>
      <v-snackbar
        v-model="exceptionSnackbar"
        class="exception-snack"
        :timeout="7500"
        height="100px"
        top
      >
        <p>A problem has occured loading data. Please try again later or contact us via Twitter. (@VITEtools)
          <a href="https://twitter.com/VITEtools" target="_blank" class="tweet-link error">
            <i class='fab fa-twitter'/>
          </a>
        </p>
        <template v-slot:action="{ attrs }">
          <v-btn
            color="blue"
            text
            v-bind="attrs"
            @click="exceptionSnackbar = false"
          >
            <p class="close-button">x</p>
          </v-btn>
        </template>
      </v-snackbar>
      <contact-footer/>
    </div>
  </div>
</template>

<script>
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);
import ViteInput from "../components/ViteInput.vue";
import { copyToClipboard, customCurrencySort, getColorForRatio, getColorForStatus, getCurrentCycle, isViteAddress } from '../helpers/componentHelper';
import ContactFooter from '../components/ContactFooter.vue';
import TransactionDetails from '../components/TransactionDetails.vue';
export default {
  components: {
    ViteInput,
    ContactFooter,
    TransactionDetails,
  },
  data: function() {
    return {
      dialog: !this.$store.state.globalViteAddress,
      viteAddress: this.$store.state.globalViteAddress,
      snackbar: false,
      errorSnackbar: false,
      exceptionSnackbar: false,
      search: "",
      cycle: this.getCurrentCycle(),
      tokenGraph: null
    }
  },
  methods: {
    async getListData() {
      if (this.cycle >= 683 && this.cycle <= getCurrentCycle()) {
        await this.$store.dispatch("wallet/getNodeListData", {viteAddress: this.viteAddress, cycle: this.cycle});
      }
    },
    async getData() {
      await this.$store.dispatch("wallet/initLoading");
      const basicCall = this.$store.dispatch("wallet/getBasicWalletData", this.viteAddress);
      const tokenCall = this.$store.dispatch("wallet/getTokenData", this.viteAddress);
      const transactionsCall = this.$store.dispatch("wallet/getTransactionListData", this.viteAddress);
      await basicCall;
      if (await tokenCall) {
        this.createTokenGraph();
      }
      await this.getListData();
      await transactionsCall;
      this.exceptionSnackbar = this.$store.state.wallet.exception;
    },
    getCurrentCycle: getCurrentCycle,
    getColorForRatio: getColorForRatio,
    getColorForStatus: getColorForStatus,
    customSort: customCurrencySort,
    setViteAddress() {
      if (isViteAddress(this.viteAddress)) {
        this.$store.state.globalViteAddress = this.viteAddress;
        this.dialog = false;
        this.getData();
      } else {
        this.errorSnackbar = true;
      }
    },
    copyToClipboard(toCopy) {
      this.snackbar = true;
      copyToClipboard(toCopy);
    },
    createTokenGraph() {
      let ctx = document.getElementById("token-graph");
      this.tokenGraph = new Chart(ctx, {
        type: "pie",
        data: {
          labels: this.$store.state.wallet.tokenGraphData.symbols,
          datasets: [{
            data: this.$store.state.wallet.tokenGraphData.usdt_value,
            hoverOffset: 20,
            backgroundColor: this.$store.state.wallet.tokenGraphData.background,
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          offset: 1
        }
      });
    }
  },
  mounted() {
    if (isViteAddress(this.$store.state.globalViteAddress)) {
      this.getData();
    }
  }
}
</script>

<style>
.v-dialog {
  max-width: 600px !important;
}

.no-address, .wallet-content {
  flex-basis: 100%;
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}

.no-address {
  height: 100vh;
  align-items: center;
}

.open-dialog-card {
  height: 200px;
}

.open-dialog-card h2 {
  flex-basis: 100%;
  text-align: center;
  font-size: 1.8em;
  color: var(--blue-dark);
  margin: 25px 5px 0;
}

.modal-content, .open-dialog-card {
  position: relative;
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  background: white;
  background: linear-gradient(270deg, #fef9f6 0%, #f6fafe 100%);
  box-shadow: 6px 6px 15px rgba(0, 0, 0, 0.3);
  padding: 5px;
  border-radius: 25px;
  min-height: 270px;
}

.modal-content h3 {
  margin: 20px;
  text-align: center;
  color: var(--blue-dark);
}

.modal-content > div {
  margin: 15px 25px 0;
}

.modal-content > div:first-of-type {
  width: 100%;
}

.button-container {
  display: flex;
  justify-content: flex-end;
}

.submit {
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  font-size: 18pt;
  font-weight: 300;
  border-radius: 10px;
  height: 45px;
  width: 140px;
  margin: 0 50px 10px;
  color: var(--blue-lightest);
  background: var(--orange);
  background: radial-gradient(at top right, var(--orange-light) 0%, var(--orange) 100%);
  transition: all 0.5s;
}

.submit:hover {
  background-position: 140px;
}

.close {
  position: absolute;
  top: 20px;
  right: 45px;
  font-weight: bold;
  width: 30px;
  height: 30px;
  border-radius: 100%;
}

.enter {
  width: 250px;
}

.enter:hover {
  background-position: 250px;
}

.card .headline {
  flex-basis: 100%;
  display: flex;
  justify-content: center;
}

.data-grid {
  flex-basis: 90%;
  display: grid;
  grid-template-columns: 1fr 2fr;
  grid-gap: 10px 0;
  font-size: 17px;
  max-width: 1000px;
  margin: 5px 0 30px;
}

.overview-card .button-container {
  flex-basis: 100%;
  display: flex;
  justify-content: center;
}

.overview-card .button-container button {
  margin-bottom: 10px;
}

.data-grid p {
  border-bottom: 1px solid var(--blue-lightest);
}

.data-grid p.category {
  color: var(--blue-dark);
  font-weight: 600;
  white-space: nowrap;
}

.data-grid p.value:nth-child(2) {
  color: var(--orange);
}

.data-grid p.value {
  text-align: end;
  font-size: 14px;
}

.data-grid p.value span {
  margin-left: 10px;
  cursor: pointer;
}

.data-table {
  margin-top: 25px;
  background: transparent !important;
  flex-basis: 95%;
  overflow: scroll;
}

.data-table td {
  text-align: center;
}

.node-card h2 {
  margin-bottom: 30px;
}

.node-card .search {
  max-width: 90% !important;
  margin-top: 25px;
}

.input-line {
  flex-basis: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.input-line > * {
  margin-left: 50px;
}

.input-line > p {
  margin: 0;
} 

.input-line p span {
  color: var(--blue-dark);
  font-weight: bold;
}

.input-line p.info {
  margin-left: 5px;
}

.input-line > input {
	border: none;
	border-bottom: 2px solid var(--grey);
  border-radius: 0;
	width: 80px;
	height: 30px;
  font-size: 13pt;
  padding: 3px;
  margin-left: 10px;
  text-align: center;
  background-color: rgba(0,0,0,0);
  color: var(--orange);
	transition: all .2s;
}

.input-line > input:focus {
	outline: none;
}

.input-line > input:hover {
	background-color: var(--blue-lightest);
	border-color: var(--blue);
}

.clickable-slot {
  cursor: pointer;
}

.one-line-slot {
  display: flex;
  justify-content: space-evenly;
  white-space: nowrap;
}

.wallet-token-card .subcard {
  flex-basis: 40%;
  padding: 10px 5px;
  border-radius: 25px;
  background: var(--grey-blue-transparent);
  box-shadow: inset 0 0 5px  rgba(0, 0, 0, 0.3);
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.graph-subcard {
  margin: 0 0 0 3%;
  flex-basis: 50% !important;
}

.table-subcard {
  height: fit-content;
}

.data-table.wallet-token-table {
  padding: 5px 5px 10px;
  border-radius: 25px;
  background-color: rgb(228, 233, 238) !important;
  box-shadow: 6px 6px 15px rgba(0, 0, 0, 0.3);
  flex-basis: 80%;
  margin: 10px;
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  overflow: hidden;
}

#token-graph {
  padding: 15px;
  border-radius: 25px;
  background: rgb(228, 233, 238);
  box-shadow: 6px 6px 15px rgba(0, 0, 0, 0.3);
  width: 100% !important;
}

@media (max-width: 750px) {
  .data-grid {
    grid-template-columns: 1fr;
  }

  .data-grid .category {
    border-bottom: none;
  }

  .data-grid p.value {
    text-align: left;
    padding-left: 50px;
    word-break: break-all;
  }

  .input-line {
    flex-wrap: wrap;
  }

  .input-line > * {
    margin-left: 0;
  }

  .input-line .button-container {
    margin: 15px 0 0;
    flex-basis: 100%;
    display: flex;
    justify-content: center;
  }

  .transaction-card {
    overflow: scroll;
  }

  .transaction-card .v-data-table {
    max-width: 90%;
  }

  .wallet-token-card .subcard {
    flex-basis: 95% !important;
    margin: 20px 0 0 0;
  }
}

@media (max-width: 500px) {
  .modal-content h3 {
    margin-top: 50px;
  }

  .close {
    top: 20px;
    right: 20px;
  }
}
</style>