<template>
  <div class="content-container" id="whales">
    <div class="table-card overview-card card">
      <div class="overview-headline">
        <h2>Whale Transactions</h2>
        <v-btn
          @click="changeTimespan()"
          color="#06254b"
          dark
        >{{timespan}} <i class="fas fa-sync"/></v-btn>
      </div>
      <div class="overview-counts">
        <div class="count-card">
          <h4>
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <span v-bind="attrs" v-on="on" class="clickable-slot">
                  Large Transactions
                </span>
              </template>
              <span>> $ 500,000</span>
            </v-tooltip>
          </h4>
          <div class="count-line">
            <p>🐳</p>
            <p>{{this.$store.state.whales.basicWhaleData.current[0]}} 
              <span v-if="this.$store.state.whales.basicWhaleData.change[0] > -1" class="positive-change">(+{{this.$store.state.whales.basicWhaleData.change[0]}})</span>
              <span v-else class="negative-change">({{this.$store.state.whales.basicWhaleData.change[0]}})</span>
            </p>
          </div>
        </div>
        <div class="count-card">
          <h4>
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <span v-bind="attrs" v-on="on" class="clickable-slot">
                  Medium Transactions
                </span>
              </template>
              <span>$ 100,000 - $ 500,000</span>
            </v-tooltip>
          </h4>
          <div class="count-line">
            <p>🐬</p>
            <p>{{this.$store.state.whales.basicWhaleData.current[1]}} 
              <span v-if="this.$store.state.whales.basicWhaleData.change[1] > -1" class="positive-change">(+{{this.$store.state.whales.basicWhaleData.change[1]}})</span>
              <span v-else class="negative-change">({{this.$store.state.whales.basicWhaleData.change[1]}})</span>
            </p>
          </div>
        </div>
        <div class="count-card">
          <h4>
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <span v-bind="attrs" v-on="on" class="clickable-slot">
                  Small Transactions
                </span>
              </template>
              <span>$ 50,000 - $ 100,000</span>
            </v-tooltip>
          </h4>
          <div class="count-line">
            <p>🐠</p>
            <p>{{this.$store.state.whales.basicWhaleData.current[2]}} 
              <span v-if="this.$store.state.whales.basicWhaleData.change[2] > -1" class="positive-change">(+{{this.$store.state.whales.basicWhaleData.change[2]}})</span>
              <span v-else class="negative-change">({{this.$store.state.whales.basicWhaleData.change[2]}})</span>
            </p>
          </div>
        </div>
      </div>
      <div v-if="!this.$store.state.whales.loading.baseWhaleLoading" class="overview-chart">
         <canvas id="overview-graph"></canvas>
      </div>
      <div v-else class="overview-chart loading">
        <v-progress-circular
            indeterminate
            color="#e4e9ee"
            class="loading-spinner"
            :size="50"
        />
      </div>
    </div>
    <div class="top-table-card table-card card">
      <h2>Top 10 Whale Transactions <span>(since 06/2021)</span></h2>
      <div v-if="!this.$store.state.whales.loading.topWhaleLoading" class="table-wrapper">
        <v-data-table :headers="this.$store.state.whales.topWhaleData.header" :items="this.$store.state.whales.topWhaleData.items" :items-per-page="10" class="data-table top-10" hide-default-footer>
          <template v-slot:item.date="{ item }">
            <span class="one-line-slot">{{ item.date }}</span>
          </template>
          <template v-slot:item.rank="{ item }">
            <v-chip
              :color="getColorForRank(item.rank)"
              dark
            >
              {{ item.rank }}
            </v-chip>
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
          <template v-slot:item.tweet="{ item }">
            <v-tooltip top>
              <template v-slot:activator="{ on, attrs }">
                <span v-bind="attrs" v-on="on">
                  <a v-bind:href="item.tweet_link" target="_blank" class="tweet-link">
                    <i class='fab fa-twitter'/>
                  </a>
                </span>
              </template>
              <span>Open Twitter</span>
            </v-tooltip>
          </template>
          <template v-slot:item.details="{ item }">
              <transaction-details :item="item"/>
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
    <div class="table-card address-card card">
      <h2>Top 10 Whale Addresses</h2>
      <div v-if="!this.$store.state.whales.loading.addressWhaleLoading" class="table-wrapper">
        <v-data-table :headers="this.$store.state.whales.addressWhaleData.header" :items="this.$store.state.whales.addressWhaleData.items" :items-per-page="10" class="data-table top-10" hide-default-footer>
          <template v-slot:item.rank="{ item }">
            <v-chip
              :color="getColorForRank(item.rank)"
              dark
            >
              {{ item.rank }}
            </v-chip>
          </template>
          <template v-slot:item.address_short="{ item }">
            <v-tooltip top>
              <template v-slot:activator="{ on, attrs }">
                <span v-bind="attrs" v-on="on" class="one-line-slot">
                  {{item.address_short}}
                  <span v-on:click="copyToClipboard(item.address)" class="clickable-slot"><i class="fas fa-copy"/></span>
                </span>
              </template>
              <span>{{item.address}}</span>
            </v-tooltip>
          </template>
          <template v-slot:item.received_string="{ item }">
            <p class="pre">{{ item.received_string }}</p>
          </template>
          <template v-slot:item.sent_string="{ item }">
            <p class="pre">{{ item.sent_string }}</p>
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
    <div class="table-card time-graph-card card">
      <div v-if="!this.$store.state.whales.loading.weekdayWhaleLoading" class="graph-card">
        <h2>Whales Per Weekday <span>(average)</span></h2>
        <canvas id="weekday-graph"></canvas>
      </div>
      <div v-else class="graph-card loading">
        <v-progress-circular
          indeterminate
          color="#e4e9ee"
          class="loading-spinner"
          :size="50"
        />
      </div>
      <div v-if="!this.$store.state.whales.loading.whalesPerWeekLoading" class="graph-card">
        <h2>Whales Per Week</h2>
        <canvas id="week-graph"></canvas>
      </div>
      <div v-else class="graph-card loading">
        <v-progress-circular
          indeterminate
          color="#e4e9ee"
          class="loading-spinner"
          :size="50"
        />
      </div>
    </div>
    <div class="current-table-card table-card card" data-app>
      <h2>Current Whale Transactions <span>(last 1000)</span></h2>
      <div v-if="!this.$store.state.whales.loading.currentWhaleLoading" class="table-wrapper">
        <v-data-table :headers="this.$store.state.whales.currentWhaleData.header" :items="this.$store.state.whales.currentWhaleData.items" :custom-sort="customSort" :items-per-page="10" class="data-table">
          <template v-slot:item.date="{ item }">
            <span class="one-line-slot">{{ item.date }}</span>
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
          <template v-slot:item.tweet="{ item }">
              <v-tooltip top>
              <template v-slot:activator="{ on, attrs }">
                <span v-bind="attrs" v-on="on">
                  <a v-bind:href="item.tweet_link" target="_blank" class="tweet-link">
                    <i class='fab fa-twitter'/>
                  </a>
                </span>
              </template>
              <span>Open Twitter</span>
            </v-tooltip>
          </template>
          <template v-slot:item.details="{ item }">
              <transaction-details :item="item"/>
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
    </div>
    <contact-footer/>
  </div>
</template>

<script>
import { Chart, registerables } from 'chart.js';
import { copyToClipboard, customCurrencySort, getColorForRank } from '../helpers/componentHelper';
import TransactionDetails from '../components/TransactionDetails.vue';
import ContactFooter from '../components/ContactFooter.vue';
Chart.register(...registerables);
export default {
  components: { TransactionDetails, ContactFooter },
  data: () => ({
    timespan: "last 7 days",
    days: 7,
    overviewGraph: null,
    weekdayGraph: null,
    weekGraph: null,
    snackbar: false,
    exceptionSnackbar: false,
  }),
  methods: {
    customSort: customCurrencySort,
    async getData() {
      await this.$store.dispatch("whales/initLoading");
      const overviewCall = this.getOverviewGraphData(this.days);
      const currentCall = this.$store.dispatch("whales/getCurrentWhaleData");
      const topCall = this.$store.dispatch("whales/getTopWhaleData");
      const addressCall = this.$store.dispatch("whales/getAddressWhaleData");
      const weekdayCall = this.$store.dispatch("whales/getWeekdayWhaleData")
      const perWeekCall = this.$store.dispatch("whales/getWhalesPerWeekData");
      if (await overviewCall) {
        this.createOverviewGraph();
      }
      await currentCall;
      await topCall;
      await addressCall;
      if (await weekdayCall) {
        this.createWeekdayGraph();
      }
      if (await perWeekCall) {
        this.createWhalesPerWeekGraph();
      }
      this.exceptionSnackbar = this.$store.state.whales.exception;
    },
    async getOverviewGraphData(days) {
      return await this.$store.dispatch("whales/getBasicWhaleData", days);
    },
    async changeTimespan() {
      switch (this.days) {
        case 7:
          this.timespan = "last 31 days";
          this.days = 31;
          break;
        case 31:
          this.timespan = "last 24 hours";
          this.days = 1;
          break;
        default:
          this.timespan = "last 7 days";
          this.days = 7;
          break;
      }
      await this.getOverviewGraphData(this.days);
      this.createOverviewGraph();
    },
    copyToClipboard(toCopy) {
      this.snackbar = true;
      copyToClipboard(toCopy);
    },
    getColorForRank: getColorForRank,
    createOverviewGraph() {
      let canvasWrapper = document.getElementsByClassName("overview-chart")[0];
      let oldCanvas = document.getElementById("overview-graph");
      canvasWrapper.removeChild(oldCanvas);
      let newCanvas = document.createElement("canvas");
      newCanvas.setAttribute("id", "overview-graph");
      canvasWrapper.appendChild(newCanvas);
      this.overviewGraph = new Chart(newCanvas, {
        type: "bar",
        data: {
          labels: ["🐳", "🐬", "🐠"],
          datasets: [{
            data: this.$store.state.whales.basicWhaleData.previous,
            label: "Last Transactions",
            backgroundColor: "rgba(230, 99, 18, 0.2)",
            barPercentage: 1,
          },
          {
            data: this.$store.state.whales.basicWhaleData.current,
            label: "Transactions",
            backgroundColor: "rgba(0, 83, 184, 0.6)",
            borderColor: "#0053b8",
            borderWidth: 1,
            barPercentage: 1,
          }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              ticks: {
                font: {
                  size: 25
                }
              }
            },
            y: {
              borderColor: "#031326",
            }
          },
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              enabled: false
            }
          }
        }
      });
    },
    createWeekdayGraph() {
      let ctx = document.getElementById("weekday-graph");
      this.weekdayGraph = new Chart(ctx, {
        type: "bar",
        data: {
          labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
          datasets: [{
            data: this.$store.state.whales.weekdayWhaleData.small,
            label: "🐠",
            backgroundColor: "rgba(230, 99, 18, 0.6)",
            borderColor: "rgb(230, 99, 18)",
            borderWidth: 1,
          },
          {
            data: this.$store.state.whales.weekdayWhaleData.medium,
            label: "🐬",
            backgroundColor: "rgba(18, 114, 230, 0.6)",
            borderColor: "rgb(18, 114, 230)",
            borderWidth: 1,
          },
          {
            data: this.$store.state.whales.weekdayWhaleData.large,
            label: "🐳",
            backgroundColor: "rgba(92, 163, 0, 0.6)",
            borderColor: "rgb(92, 163, 0)",
            borderWidth: 1,
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              stacked: true,
              ticks: {
                font: {
                  size: 16
                }
              }
            },
            y: {
              stacked: true,
            }
          },
          plugins: {
            legend: {
              labels: {
                font: {
                  size: 20
                }
              }
            }
          }
        }
      });
    },
    createWhalesPerWeekGraph() {
      let ctx = document.getElementById("week-graph");
      this.weekdayGraph = new Chart(ctx, {
        type: "bar",
        data: {
          labels: this.$store.state.whales.whalesPerWeekData.cw,
          datasets: [{
            data: this.$store.state.whales.whalesPerWeekData.count.small,
            label: "🐠",
            backgroundColor: "rgba(230, 99, 18, 0.6)",
            borderColor: "rgb(230, 99, 18)",
            borderWidth: 1,
          },
          {
            data: this.$store.state.whales.whalesPerWeekData.count.medium,
            label: "🐬",
            backgroundColor: "rgba(18, 114, 230, 0.6)",
            borderColor: "rgb(18, 114, 230)",
            borderWidth: 1,
          },
          {
            data: this.$store.state.whales.whalesPerWeekData.count.large,
            label: "🐳",
            backgroundColor: "rgba(92, 163, 0, 0.6)",
            borderColor: "rgb(92, 163, 0)",
            borderWidth: 1,
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              stacked: true,
              ticks: {
                font: {
                  size: 14
                }
              },
              title: {
                text: "Calendar Week",
                display: true,
                font: {
                  size: 20
                }
              }
            },
            y: {
              stacked: true,
            }
          },
          plugins: {
            legend: {
              labels: {
                font: {
                  size: 20
                }
              }
            }
          }
        }
      });
    }
  },
  mounted() {
    this.getData();
  }
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

.table-card {
  flex-basis: 90%;
  min-width: 300px;
  padding: 5px 5px 10px;
  border-radius: 25px;
  background: white;
  background: linear-gradient(270deg, #fef9f6 0%, #f6fafe 100%);
  box-shadow: 6px 6px 15px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  margin: 0 0 30px 0;
}

.overview-card {
  padding: 5px 5px 20px;
}

.table-card h2 {
  color: var(--blue-dark);
  font-size: 1.8em;
  margin: 20px 5px 20px;
  text-align: center;
}

.current-table-card h2 span, .top-table-card h2 span {
  font-weight: 300;
  font-size: 0.8em;
  margin: 0 0 0 10px;
}

.data-table {
  background: transparent !important;
}

.data-table td, .data-table th {
  text-align: center;
}

.clickable-slot {
  cursor: pointer;
}

.tweet-link {
  text-decoration: none;
}

.one-line-slot {
  display: flex;
  justify-content: space-evenly;
  white-space: nowrap;
}

.overview-headline {
  flex-basis: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.overview-headline h2 {
  margin-right: 20px;
}

.overview-counts {
  flex-basis: 40%;
  padding: 10px 5px;
  border-radius: 25px;
  background: var(--grey-blue-transparent);
  box-shadow: inset 0 0 5px  rgba(0, 0, 0, 0.3);
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.count-card {
  padding: 5px 5px 10px;
  border-radius: 25px;
  background: rgb(228, 233, 238);
  box-shadow: 6px 6px 15px rgba(0, 0, 0, 0.3);
  flex-basis: 80%;
  margin: 10px;
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}

.count-card h4 {
  flex-basis: 100%;
  text-align: center;
  margin: 5px 0 15px;
}

.count-line {
  flex-basis: 100%;
  display: flex;
  justify-content: flex-start;
  font-size: 1.5em;
} 

.count-line p:first-child {
  flex-basis: 40%;
  text-align: center;
}

.count-line p {
  text-align: start;
}

span.positive-change {
  color: rgb(6, 189, 0);
}

span.negative-change {
  color: rgb(226, 0, 0);
}

.overview-chart {
  flex-basis: 50%;
  padding: 10px;
  margin: 0 0 0 3%;
  border-radius: 25px;
  background: var(--grey-blue-transparent);
  box-shadow: inset 0 0 5px  rgba(0, 0, 0, 0.3);
  display: flex;
  justify-content: center;
  align-items: center;
}

#week-graph, #weekday-graph, #overview-graph {
  padding: 15px;
  border-radius: 25px;
  background: rgb(228, 233, 238);
  box-shadow: 6px 6px 15px rgba(0, 0, 0, 0.3);
  width: 100% !important;
}

#week-graph, #weekday-graph {
  max-height: 80% !important;
}

.time-graph-card {
  flex-basis: 40%;
  margin-left: 2%;
  display: flex;
  justify-content: center;
  padding: 10px;
  max-height: 1040px;
}

.graph-card {
  padding: 10px;
  border-radius: 25px;
  background: var(--grey-blue-transparent);
  box-shadow: inset 0 0 5px  rgba(0, 0, 0, 0.3);
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  height: 48%;
}

.graph-card h2 {
  flex-basis: 100%;
  text-align: center;
  color: var(--blue-lightest);
}

.graph-card h2 span {
  font-weight: 400;
  font-size: 0.8em
}

.address-card {
  flex-basis: 48%;
}

.pre {
  white-space: pre;
  text-align: center;
  line-height: 30px;
}

@media (max-width: 1400px) {
  .address-card, .time-graph-card {
    flex-basis: 90%;
  }

  .time-graph-card {
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-evenly;
    margin-left: 0;
    min-height: 500px;
    padding: 5px
  }

  .graph-card {
    flex-basis: 45%;
    height: 90%;
  }

  #weekday-graph {
    max-height: 70% !important;
  }
}

@media (max-width: 800px) {
  .time-graph-card {
    min-height: 800px;
    max-height: none;
  }

  .time-graph-card h2 {
    margin: 15px 0 5px;
  }

  .graph-card {
    flex-basis: 95%;
    height: 48%;
  }
}

@media (max-width: 750px) {
  .overview-counts {
    flex-basis: 90%;
  }

  .overview-chart {
    flex-basis: 90%;
    margin: 10px 0;
  }

  .overview-headline {
    flex-wrap: wrap;
    margin: 0 0 20px;
  }

  .overview-headline h2 {
    margin-right: 0;
    flex-basis: 100%;
  }
}

@media (max-width: 600px) {
  .pre {
    white-space: normal;
  }
}

@media (max-width: 500px) {
  .content-container {
    margin: 20px 10px;
  }

  .table-card {
    flex-basis: 95% !important;
  }

  .current-table-card h2, 
  .time-graph-card h2, 
  .top-table-card h2 {
    font-size: 1.3em;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
  }

  .current-table-card h2 span, 
  .time-graph-card h2 span,
  .top-table-card h2 span {
    margin: 0;
    flex-basis: 100%;
  }
}

/* vuetify style changes */

.v-data-table {
  min-width: 90%;
}

.v-data-footer {
  justify-content: center;
}

.v-data-footer__select {
  margin: 0 10px;
}

.v-data-footer__select .v-select {
  margin: 0 10px;
}

.address-card .v-data-table-header th:first-of-type,
.top-table-card .v-data-table-header th:first-of-type {
  font-size: 1.25em;
}

@media (max-width: 500px) {
  .v-data-footer__select {
    margin: 0 5px;
  }

  .v-data-footer__select .v-select {
    margin: 0 5px;
  }
}
</style>