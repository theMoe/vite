<template>
  <div class="content-container" id="transactions" data-app>
    <router-link class="transactions-link" to="/wallet">
        <p class="transactions-info">
            Looking for transactions of a specific VITE address? 
            <i class="fas fa-arrow-right"/>
        </p>
    </router-link>
    <router-link class="transactions-link" to="/whales">
        <p class="transactions-info">
            Looking for statistics and lists of whale transactions only? 
            <i class="fas fa-arrow-right"/>
        </p>
    </router-link>
    <div class="card">
      <div class="main-headline">
        <h2>Last Transactions</h2>
      </div>
      <div v-if="!this.$store.state.transactions.loading.listLoading" class="table-wrapper">
        <v-data-table :headers="this.$store.state.transactions.currentTransactionsTableData.header" :items="this.$store.state.transactions.currentTransactionsTableData.items" :items-per-page="50" class="data-table transactions-table">
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
import { copyToClipboard } from "../helpers/componentHelper";
import TransactionDetails from "../components/TransactionDetails.vue";
import ContactFooter from '../components/ContactFooter.vue';
export default {
    components: {
        TransactionDetails,
        ContactFooter
    },
    data: () => ({
        snackbar: false,
        exceptionSnackbar: false
    }),
    methods: {
        copyToClipboard(toCopy) {
          this.snackbar = true;
          copyToClipboard(toCopy);
        },
        async getTransactionsDataFromApi() {
          await this.$store.dispatch("transactions/initLoading");
          await this.$store.dispatch("transactions/getCurrentTransactionsList");
          this.exceptionSnackbar = this.$store.state.transactions.exception;
        },
    },
    mounted() {
        this.getTransactionsDataFromApi();
    }
}
</script>

<style>
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

.transactions-info {
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

.transactions-info:hover {
  background: var(--orange-lightest);
}

.transactions-info * {
  margin-left: 10px !important;
  font-size: 1.2em;
}

.transactions-link {
  text-decoration: none;
  margin: 0 20px 20px;
  min-width: 70%;
}
</style>