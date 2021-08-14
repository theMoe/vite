<template>
  <div class="content-container" id="tokens" data-app>
    <div class="token-card card">
      <h2>Tokens</h2>
      <div v-if="!this.$store.state.tokens.loading" class="table-wrapper">
        <v-data-table
          :headers="this.$store.state.tokens.tokenTableData.header"
          :items="this.$store.state.tokens.tokenTableData.items"
          :items-per-page="20"
          :custom-sort="customSort"
          class="data-table token-table"
        >
          <template v-slot:item.owner="{ item }">
            <v-tooltip top>
              <template v-slot:activator="{ on, attrs }">
                <span v-bind="attrs" v-on="on" class="one-line-slot">
                  {{ item.owner_short }}
                  <span
                    v-on:click="copyToClipboard(item.owner)"
                    class="clickable-slot"
                    ><i class="fas fa-copy"
                  /></span>
                </span>
              </template>
              <span>{{ item.owner }}</span>
            </v-tooltip>
          </template>
          <template v-slot:item.id_short="{ item }">
            <v-tooltip top>
              <template v-slot:activator="{ on, attrs }">
                <span v-bind="attrs" v-on="on" class="one-line-slot">
                  {{ item.id_short }}
                  <span
                    v-on:click="copyToClipboard(item.tokenId)"
                    class="clickable-slot"
                    ><i class="fas fa-copy"
                  /></span>
                </span>
              </template>
              <span>{{ item.tokenId }}</span>
            </v-tooltip>
          </template>
          <template v-slot:item.details="{ item }">
            <token-details :item="item" />
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
import TokenDetails from "../components/TokenDetails.vue";
import {
  copyToClipboard,
  customCurrencySort,
} from "../helpers/componentHelper";
export default {
  components: { TokenDetails, ContactFooter },
  data: () => ({
    snackbar: false,
    exceptionSnackbar: false,
  }),
  methods: {
    copyToClipboard(toCopy) {
      this.snackbar = true;
      copyToClipboard(toCopy);
    },
    customSort: customCurrencySort,
  },
  async mounted() {
    await this.$store.dispatch("tokens/initLoading");
    await this.$store.dispatch("tokens/getTokenData");
    this.exceptionSnackbar = this.$store.state.tokens.exception;
  },
};
</script>

<style scoped>
.token-card h2 {
  font-size: 2em;
}

@media (max-width: 500px) {
  .content-container {
    margin: 20px 10px;
  }

  .token-card {
    flex-basis: 95% !important;
  }
}
</style>
