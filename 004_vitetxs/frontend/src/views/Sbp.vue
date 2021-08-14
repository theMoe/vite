<template>
  <div class="content-container" id="sbp" data-app>
    <div class="main-card card">
      <div class="main-headline">
        <h2>SBP Stats</h2>
      </div>
      <div v-if="!this.$store.state.sbp.loading" class="table-wrapper">
        <v-data-table
          :headers="this.$store.state.sbp.sbpTableData.header"
          :items="this.$store.state.sbp.sbpTableData.items"
          :items-per-page="70"
          :custom-sort="customSort"
          class="data-table sbp-table"
          hide-default-footer
        >
          <template v-slot:item.rank="{ item }">
            <v-chip :color="getColorForRank(item.rank)" dark>
              {{ item.rank }}
            </v-chip>
          </template>
          <template v-slot:item.address_short="{ item }">
            <v-tooltip top>
              <template v-slot:activator="{ on, attrs }">
                <span v-bind="attrs" v-on="on" class="one-line-slot">
                  {{ item.address_short }}
                  <span
                    v-on:click="copyToClipboard(item.block_producing_address)"
                    class="clickable-slot"
                    ><i class="fas fa-copy"
                  /></span>
                </span>
              </template>
              <span>{{ item.address }}</span>
            </v-tooltip>
          </template>
          <template v-slot:item.details="{ item }">
            <sbp-details :item="item" />
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
      <v-snackbar v-model="snackbar" :timeout="2000" class="copy-snackbar">
        Copied!
        <template v-slot:action="{ attrs }">
          <v-btn color="blue" text v-bind="attrs" @click="snackbar = false">
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
        <p>
          A problem has occured loading data. Please try again later or contact
          us via Twitter. (@VITEtools)
          <a
            href="https://twitter.com/VITEtools"
            target="_blank"
            class="tweet-link error"
          >
            <i class="fab fa-twitter" />
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
    <contact-footer />
  </div>
</template>

<script>
import ContactFooter from "../components/ContactFooter.vue";
import SbpDetails from "../components/SbpDetails.vue";
import {
  copyToClipboard,
  customCurrencySort,
  getColorForRank,
} from "../helpers/componentHelper";
export default {
  components: { SbpDetails, ContactFooter },
  data: () => ({
    snackbar: false,
    exceptionSnackbar: false,
  }),
  methods: {
    copyToClipboard(toCopy) {
      this.snackbar = true;
      copyToClipboard(toCopy);
    },
    async getSbpDataFromApi() {
      await this.$store.dispatch("sbp/initLoading");
      await this.$store.dispatch("sbp/getSbpList");
      this.exceptionSnackbar = this.$store.state.sbp.exception;
    },
    customSort: customCurrencySort,
    getColorForRank: getColorForRank,
  },
  mounted() {
    this.getSbpDataFromApi();
  },
};
</script>

<style>
.main-headline {
  flex-basis: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* vuetify style changes */

.v-data-table {
  min-width: 95%;
}

#sbp .main-card .v-data-table-header th:first-of-type {
  font-size: 1.25em;
  padding-left: 15px;
}
</style>
