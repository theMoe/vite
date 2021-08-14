<template>
  <div class="content-container" id="dashboard" data-app>
    <div class="overview-card dashboard-card card">
      <h2>VITE Overview</h2>
      <div v-if="!this.$store.state.dashboard.loading.countsLoading" class="count-grid">
        <div class="count">
          <h4>Block Height</h4>
          <p>{{this.$store.state.dashboard.counts.block_height}}</p>
        </div>
        <div class="count">
          <h4>Price</h4>
          <p>{{this.$store.state.dashboard.counts.price}}</p>
        </div>
        <div class="count">
          <h4>Tokens</h4>
          <p>{{this.$store.state.dashboard.counts.tokens}}</p>
        </div>
        <div class="count">
          <h4>Active Accounts</h4>
          <p>{{this.$store.state.dashboard.counts.total_accounts}}</p>
        </div>
        <div class="count">
          <h4>Transactions Last Day</h4>
          <p>{{this.$store.state.dashboard.counts.transactions_last_day}}</p>
        </div>
        <div class="count">
          <h4>Online Nodes</h4>
          <p>{{this.$store.state.dashboard.counts.online_nodes}}</p>
        </div>
        <div class="count">
          <h4>SBP</h4>
          <p>{{this.$store.state.dashboard.counts.super_nodes}}</p>
        </div>
        <div class="count">
          <h4>Total Supply</h4>
          <p>{{this.$store.state.dashboard.counts.total_supply}}</p>
        </div>
        <div class="count filler">
        </div>
      </div>
      <div v-else class="loading">
        <v-progress-circular
            indeterminate
            color="#06254b"
            class="loading-spinner"
            :size="50"
        />
      </div>
    </div>
    <div class="reward-card dashboard-card card">
      <h2>Daily Rewards <span>(per node)</span></h2>
      <div v-if="!this.$store.state.dashboard.loading.rewardLoading" class="graph-wrapper">
        <canvas id="reward-graph"></canvas>
      </div>
      <div v-else class="graph-wrapper loading">
        <v-progress-circular
            indeterminate
            color="#06254b"
            class="loading-spinner"
            :size="50"
        />
      </div>
    </div>
    <div class="transaction-card dashboard-card card">
      <div class="main-headline">
        <h2>Last Transactions</h2>
      </div>
      <div v-if="!this.$store.state.dashboard.loading.listLoading" class="table-wrapper">
        <v-data-table :headers="this.$store.state.dashboard.transactionListData.header" :items="this.$store.state.dashboard.transactionListData.items" :items-per-page="10" class="data-table transactions-table" hide-default-footer>
          <template v-slot:item.tx_hash_short="{ item }">
            <v-tooltip top>
              <template v-slot:activator="{ on, attrs }">
                <span v-bind="attrs" v-on="on" class="one-line-slot">
                  {{item.tx_hash_short}}
                  <span v-on:click="copyToClipboard(item.tx_hash)" class="clickable-slot"><i class="fas fa-copy"/></span>
                </span>
              </template>
              <span>{{item.tx_hash}}</span>
            </v-tooltip>
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
    </div>
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
</template>

<script>
import { Chart, registerables } from 'chart.js';
import ContactFooter from '../components/ContactFooter.vue';
import { copyToClipboard } from '../helpers/componentHelper';
import TransactionDetails from '../components/TransactionDetails.vue';
Chart.register(...registerables);
export default {
  components: {
    ContactFooter,
    TransactionDetails
  },
  data: () => ({
    rewardGraph: null,
    snackbar: false,
    exceptionSnackbar: false,
  }),
  methods: {
    copyToClipboard: copyToClipboard,
    async getData() {
      await this.$store.dispatch("dashboard/initLoading");
      const countCall =  this.$store.dispatch("dashboard/getDashboardCounts");
      const rewardCall = this.$store.dispatch("dashboard/getRewardGraphData");
      const transactionsCall = this.$store.dispatch("dashboard/getLastTransactions", 10);
      await rewardCall;
      if (rewardCall) {
        this.createRewardGraph();
      }
      await transactionsCall;
      await countCall;
      
      this.exceptionSnackbar = this.$store.state.dashboard.exception
    },
    createRewardGraph() {
      let ctx = document.getElementById("reward-graph");
      this.rewardGraph = new Chart(ctx, {
        type: "line",
        data: {
          labels: this.$store.state.dashboard.rewardGraphData.dates,
          datasets: [{
            data: this.$store.state.dashboard.rewardGraphData.amount,
            label: "amount in VITE",
            yAxisID: "vite",
            tension: 0.1,
            backgroundColor: "#1272e6",
            borderColor: "#90bef3",
            color: "#1272e6"
          }, {
            data: this.$store.state.dashboard.rewardGraphData.usdt_values,
            label: "amount in USDT",
            yAxisID: "usdt",
            tension: 0.1,
            backgroundColor: "#e66312",
            borderColor: "#f3b690",
            color: "#e66312"
          }]
        },
        options: {
          maintainAspectRatio: false,
          scales: {
              'vite': {
                  type: "linear",
                  title: {
                    text: "VITE",
                    display: true,
                    color: "#1272e6"
                  },
                  position: "left",
                  suggestedMin: 0,
                  suggestedMax: 20,
                  grid: {
                    borderColor: "#1272e6"
                  },
                  ticks: {
                    color: "#1272e6"
                  }
              },
              'usdt': {
                  type: "linear",
                  title: {
                    text: "USDT",
                    display: true,
                    color: "#e66312",
                  },
                  position: "right",
                  suggestedMin: 0,
                  suggestedMax: 5,
                  grid: {
                    borderColor: "#e66312"
                  },
                  ticks: {
                    color: "#e66312"
                  }
              }
          },
          plugins: {
            legend: {
              display: false
            }
          }
        }
      })
    }
  },
  mounted() {
    this.getData();
  },
}
</script>

<style>
.content-container {
  flex-basis: calc(100% - 250px);
  margin: 30px 30px;
  height: 100%;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  max-width: 1600px;
}

.transaction-card, .reward-card {
  margin: 30px 0;
}

.reward-card {
  height: 500px;
}

.count-grid {
  flex-basis: 95%;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  margin: 20px 0;
}

.count-grid .count {
  place-self: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 15px 5px;
  border: 1px solid var(--blue-light);
  border-bottom-color: transparent;
  border-right-color: transparent;
  width: 100%;
  height: 100px;
}

.count.filler {
  display: none;
}

.count h4 {
  letter-spacing: 0.02em;
  color: var(--orange);
  font-weight: 500;
  text-align: center;
  font-size: 15px;
  margin-bottom: 5px;
}

.count p {
  text-align: center;
  color: var(--blue);
  background: -webkit-linear-gradient(-85deg, var(--blue),var(--blue-dark));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 30px;
}

.graph-wrapper {
  flex-basis: 100%;
  max-height: 80%;
  overflow: auto;
}

.graph-wrapper.loading {
  display: flex;
  justify-content: center;
}

#reward-graph {
  height: 100%;
  width: 100%;
}

h2 {
  color: var(--blue-dark);
  font-size: 1.8em;
  margin: 20px;
  text-align: center;
}

h2 span {
  font-weight: 300;
  font-size: 0.8em;
}

.main-headline {
  flex-basis: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.main-headline h2 {
  color: var(--blue-dark);
  font-size: 1.8em;
  margin: 20px;
  text-align: center;
}

.transactions-table td {
  text-align: center;
}

@media (min-width: 1000px) {
  .count:nth-last-child(n + 6) {
    border-top-color: transparent;
  }

  .count:nth-child(4n - 3) {
    border-left-color: transparent;
  }
}

@media (max-width: 1000px) and (min-width: 700px) {
  .count {
    height: 95px;
  }

  .count-grid {
    grid-template-columns: repeat(3, 1fr);
  }

  .count.filler {
    display: flex;
    height: 100%;
    border-right-color: transparent !important;
  }

  .count:nth-child(3n + 1) {
    border-left-color: transparent;
  }

  .count:nth-last-child(n + 7) {
    border-top-color: transparent;
  }

  .count:last-child {
    border-right-color: var(--blue-light);
  }
}

@media (max-width: 700px) {
  .count {
    height: 90px;
  }

  .count-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .count:nth-child(2n - 1) {
    border-left-color: transparent;
  }

  .count:nth-last-child(n + 8) {
    border-top-color: transparent;
  }

  .count h4 {
    font-size: 13px;
  }

  .count p {
    font-size: 24px;
  }
} 

@media (max-width: 500px) {
  .count {
    height: 80px;
  }

  .count h4 {
    font-size: 12px;
  }

  .count p {
    font-size: 20px;
  }
}
</style>