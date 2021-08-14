<template>
  <div class="content-container" id="nodes" data-app>
    <div class="card overview-card">
      <div class="overview-headline">
        <h2>Full Node Stats</h2>
        <v-btn
          @click="changeTimespan()"
          color="#06254b"
          dark
        >{{timespan}} <i class="fas fa-sync"/></v-btn>
      </div>
      <div class="overview-stats">
        <div class="stat-card">
          <h4>Active Full Nodes</h4>
          <div class="stat-line">
            <p class="average" v-if="cycles != 1">(avg.)</p>
            <p>{{this.$store.state.nodes.basicNodeData.count[0]}} 
              <span v-if="cycles != getCurrentCycle() && this.$store.state.nodes.basicNodeData.change[0] > 0" class="positive-change">(+{{this.$store.state.nodes.basicNodeData.change[0]}})</span>
              <span v-else-if="cycles != getCurrentCycle()" class="negative-change">({{this.$store.state.nodes.basicNodeData.change[0]}})</span>
            </p>
          </div>
        </div>
        <div class="stat-card">
          <h4>
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <span v-bind="attrs" v-on="on" class="clickable-slot">
                  Rewarded Full Nodes
                </span>
              </template>
              <span>Full Nodes earn rewards by being online for >90% of the time in a circle</span>
            </v-tooltip>
          </h4>
          <div class="stat-line">
            <p class="average" v-if="cycles != 1">(avg.)</p>
            <p>{{this.$store.state.nodes.basicNodeData.count[1]}} 
              <span v-if="cycles != getCurrentCycle() && this.$store.state.nodes.basicNodeData.change[1] > 0" class="positive-change">(+{{this.$store.state.nodes.basicNodeData.change[1]}})</span>
              <span v-else-if="cycles != getCurrentCycle()" class="negative-change">({{this.$store.state.nodes.basicNodeData.change[1]}})</span>
            </p>
          </div>
        </div>
        <div class="stat-card">
          <h4>
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <span v-bind="attrs" v-on="on" class="clickable-slot">
                  Daily Rewards
                </span>
              </template>
              <span>rewards per rewarded nodes</span>
            </v-tooltip>
          </h4>
          <div class="stat-line">            
            <p class="average" v-if="cycles != 1">(avg.)</p>
            <p>{{this.$store.state.nodes.basicNodeData.rewardCount[2]}} 
              <span v-if="cycles != getCurrentCycle() && this.$store.state.nodes.basicNodeData.change[2] > 0" class="positive-change">(+{{this.$store.state.nodes.basicNodeData.change[2]}})</span>
              <span v-else-if="cycles != getCurrentCycle()" class="negative-change">({{this.$store.state.nodes.basicNodeData.change[2]}})</span>
            </p>
          </div>
        </div>
      </div>
      <div v-if="!this.$store.state.nodes.loading.basicDataLoading" class="node-chart">
         <canvas id="node-graph"></canvas>
      </div>
      <div v-else class="node-chart loading">
        <v-progress-circular
            indeterminate
            color="#e4e9ee"
            class="loading-spinner"
            :size="50"
        />
      </div>
    </div>
    <div class="card map-card">
      <div class="overview-headline">
        <h2>Node Distribution</h2>
      </div>
      <div v-if="!this.$store.state.nodes.loading.nodeMapLoading" class="map-container">
        <div class="map" ref="map"></div>
      </div>
      <div v-else class="map-container loading">
        <v-progress-circular
            indeterminate
            color="#06254b"
            class="loading-spinner"
            :size="50"
        />
      </div>
    </div>
    <router-link class="node-link" to="/wallet">
      <p class="node-info">
        Looking for full nodes of a specific VITE address? 
        <i class="fas fa-arrow-right"/>
      </p>
    </router-link>
    <div class="card list-card">
      <div class="overview-headline">
        <h2>List of all full nodes</h2>
      </div>
      <div class="input-line">
        <p>choose a <span>cycle</span>:</p>
        <input v-model="listCycle"/>
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
      <div v-if="!this.$store.state.nodes.loading.listDataLoading" class="table-wrapper">
        <v-data-table :headers="this.$store.state.nodes.nodeListData.header" :items="this.$store.state.nodes.nodeListData.items" :items-per-page="15" class="data-table node-table" multi-sort :search="search">
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
          <template v-slot:item.online_ratio="{ item }">
            <v-chip
              :color="getColorForRatio(item.online_ratio)"
              dark
              outlined
            >
              {{ item.online_ratio }}
            </v-chip>
          </template>
          <template v-slot:item.isAlive="{ item }">
            <v-chip
              :color="getColorForStatus(item.isAlive)"
              dark
              label
            >
              {{ item.isAlive }}
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
import * as am4core from "@amcharts/amcharts4/core";
import * as am4maps from "@amcharts/amcharts4/maps";
import am4geodata_worldLow from "@amcharts/amcharts4-geodata/worldLow"
import { copyToClipboard, getColorForRatio, getColorForStatus, getCurrentCycle } from '../helpers/componentHelper';
import ContactFooter from '../components/ContactFooter.vue';

Chart.register(...registerables);
export default {
  components: { ContactFooter },
  data: () => ({
    timespan: "last cycle",
    cycles: 1,
    listCycle: 0,
    snackbar: false,
    exceptionSnackbar: false,
    search: ""
  }),
  methods: {
    async getData() {
      await this.$store.dispatch('nodes/initLoading');
      const basicCall = this.$store.dispatch("nodes/getBasicNodeData", this.cycles);
      const mapCall = this.$store.dispatch("nodes/getNodeMapData");
      if (await basicCall) {
        this.createOverviewGraph();
      }
      if (await mapCall) {
        this.createMap();
      }
      await this.getListData();
      this.exceptionSnackbar = this.$store.state.nodes.exception;
    },
    getCurrentCycle: getCurrentCycle,
    getColorForRatio: getColorForRatio,
    getColorForStatus: getColorForStatus,
    copyToClipboard(toCopy) {
      this.snackbar = true;
      copyToClipboard(toCopy);
    },
    async changeTimespan() {
      switch (this.cycles) {
        case 1:
          this.timespan = "last 5 cycles";
          this.cycles = 5;
          break;
        case 5:
          this.timespan = "last 50 cycles";
          this.cycles = 50;
          break;
        default:
          this.timespan = "last cycle";
          this.cycles = 1;
          break;
      }
      await this.$store.dispatch("nodes/getBasicNodeData", this.cycles);
      this.createOverviewGraph();
    },
    createOverviewGraph() {
      let canvasWrapper = document.getElementsByClassName("node-chart")[0];
      let oldCanvas = document.getElementById("node-graph");
      canvasWrapper.removeChild(oldCanvas);
      let newCanvas = document.createElement("canvas");
      newCanvas.setAttribute("id", "node-graph");
      canvasWrapper.appendChild(newCanvas);
      this.overviewGraph = new Chart(newCanvas, {
        type: "bar",
        data: {
          labels: ["Active", "Rewarded", "Rewards"],
          datasets: [{
            data: this.$store.state.nodes.basicNodeData.lastCount,
            label: "Last Timespan",
            backgroundColor: "rgba(0, 83, 184, 0.15)",
            barPercentage: 1,
            yAxisID: "nodes",
          },
          {
            data: this.$store.state.nodes.basicNodeData.count,
            label: "Current Timespan",
            backgroundColor: "rgba(0, 83, 184, 0.6)",
            borderColor: "#0053b8",
            borderWidth: 1,
            barPercentage: 1,
            yAxisID: "nodes",
          },
          {
            data: this.$store.state.nodes.basicNodeData.lastRewardCount,
            label: "Last Timespan",
            backgroundColor: "rgba(230, 99, 18, 0.2)",
            barPercentage: 1,
            yAxisID: "rewards",
          },
          {
            data: this.$store.state.nodes.basicNodeData.rewardCount,
            label: "Current Timespan",
            backgroundColor: "rgba(230, 99, 18, 0.6)",
            borderColor: "#e66312",
            borderWidth: 1,
            barPercentage: 1,
            yAxisID: "rewards",
          },
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            'nodes': {
              title: {
                text: "Nodes",
                display: true,
                color: "#1272e6"
              },
              position: "left",
              suggestedMin: 0,
              grid: {
                borderColor: "#1272e6"
              },
              ticks: {
                color: "#1272e6"
              }
            },
            'rewards': {
              title: {
                text: "Rewards",
                display: true,
                color: "#e66312",
              },
              position: "right",
              suggestedMin: 0,
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
            },
            tooltip: {
              enabled: false
            }
          }
        }
      });
    },
    async getListData() {
      if (this.listCycle >= 683 && this.listCycle <= getCurrentCycle()) {
        await this.$store.dispatch("nodes/getNodeListData", this.listCycle);
      }  
    },
    createMap() {
      let map = am4core.create(this.$refs.map, am4maps.MapChart);

      map.geodata = am4geodata_worldLow;

      let polygonSeries = new am4maps.MapPolygonSeries();
      polygonSeries.useGeodata = true;
      polygonSeries.exclude = ["AQ"];
      map.series.push(polygonSeries);

      // Configure series
      let polygonTemplate = polygonSeries.mapPolygons.template;
      polygonTemplate.tooltipText = "{name}";
      polygonTemplate.fill = am4core.color("#ffe7d6");

      // // Create hover state and set alternative fill color
      let hs = polygonTemplate.states.create("hover");
      hs.properties.fill = am4core.color("#1272e6");

      polygonSeries.data = this.$store.state.nodes.nodeMapData.countries;

      polygonTemplate.propertyFields.fill = "fill";

      // Create image series
      let imageSeries = map.series.push(new am4maps.MapImageSeries());

      // Create a circle image in image series template so it gets replicated to all new images
      let imageSeriesTemplate = imageSeries.mapImages.template;
      let circle = imageSeriesTemplate.createChild(am4core.Circle);
      circle.radius = 4;
      circle.fill = am4core.color("#1272e6");
      circle.stroke = am4core.color("#ecf4fd");
      circle.strokeWidth = 2;
      circle.nonScaling = true;
      circle.tooltipText = "{title}";

      // Set property fields
      imageSeriesTemplate.propertyFields.latitude = "latitude";
      imageSeriesTemplate.propertyFields.longitude = "longitude";

      // Add data for the three cities
      imageSeries.data = this.$store.state.nodes.nodeMapData.cities;

      this.map = map;
    }
  },
  async mounted() {
    this.listCycle = this.getCurrentCycle();
    await this.getData();
  },
  beforeDestroy() {
    if (this.map) {
      this.map.dispose();
    }
  }
}
</script>

<style>
.overview-card {
  padding: 5px 5px 20px;
}

.tweet-link {
  text-decoration: none;
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

.overview-stats {
  flex-basis: 40%;
  padding: 10px 5px;
  border-radius: 25px;
  background: var(--grey-blue-transparent);
  box-shadow: inset 0 0 5px  rgba(0, 0, 0, 0.3);
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.stat-card {
  padding: 5px 5px 10px;
  border-radius: 25px;
  background: #e4e9ee;
  box-shadow: 6px 6px 15px rgba(0, 0, 0, 0.3);
  flex-basis: 80%;
  margin: 10px;
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}

.stat-card h4 {
  flex-basis: 100%;
  text-align: center;
  margin: 5px 0 15px;
}

.stat-line {
  flex-basis: 100%;
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  font-size: 1.5em;
} 

.stat-line .average {
  display: flex;
  align-items: center;
  margin: 0 5px 0 -30px;
  font-size: 0.6em;
  color: var(--blue-light);
  background: rgb(228, 233, 238);
  border-radius: 10px;
}

.stat-line p {
  text-align: start;
}

span.positive-change {
  color: rgb(6, 189, 0);
}

span.negative-change {
  color: rgb(226, 0, 0);
}

.node-chart {
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

#node-graph {
  padding: 15px;
  border-radius: 25px;
  background: rgb(228, 233, 238);
  box-shadow: 6px 6px 15px rgba(0, 0, 0, 0.3);
  width: 100% !important;
}

.list-card h2 {
  margin-bottom: 30px;
}

.list-card .search {
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

.data-table {
  margin-top: 25px;
  background: transparent !important;
}

.data-table td {
  text-align: center;
}

.node-info {
  color: var(--orange);
  width: 100%;
  border-radius: 10px;
  background: white;
  min-height: 40px;
  padding: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s;
}

.node-info:hover {
  background: var(--orange-lightest);
}

.node-info * {
  margin-left: 10px !important;
  font-size: 1.2em;
}

.node-link {
  text-decoration: none;
  margin: 0 20px 20px;
  min-width: 70%;
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
}

.map-container {
  flex-basis: 95%;
  border-radius: 20px;
}

.map {
  width: 100%;
  height: 500px;
}

@media (max-width: 750px) {
  .overview-stats {
    flex-basis: 90%;
  }

  .node-chart {
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
}
</style>