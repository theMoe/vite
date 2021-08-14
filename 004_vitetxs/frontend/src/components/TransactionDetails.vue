<template>
  <v-dialog class="dialog">
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        class="info-button"
        color="#06254b"
        dark
        rounded
        v-bind="attrs"
        v-on="on"
      >
        <i class="fas fa-info"></i>
      </v-btn>
    </template>
    <v-card class="detail-modal">
      <h3 class="modal-headline">Transaction</h3>
      <v-simple-table>
        <template v-slot:default>
          <tbody>
            <tr>
              <td>Hash</td>
              <td>{{ item.tx_hash }}</td>
            </tr>
            <tr>
              <td>Token</td>
              <td>{{ item.symbol }}</td>
            </tr>
            <tr>
              <td>Amount</td>
              <td>{{ item.amount_normalised }}</td>
            </tr>
            <tr v-if="parseCurrencyToNumber(item.transaction_in_usdt) !== 0">
              <td>Value in USDT</td>
              <td>{{ item.transaction_in_usdt }}</td>
            </tr>
            <tr>
              <td>From</td>
              <td>{{ item.from_address }}</td>
            </tr>
            <tr>
              <td>To</td>
              <td>{{ item.to_address }}</td>
            </tr>
            <tr>
              <td>Date</td>
              <td>{{ parseLocaleDate(item.created_at) }}</td>
            </tr>
            <tr>
              <td>Snapshot Hash</td>
              <td>{{ item.snapshot_hash }}</td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </v-card>
  </v-dialog>
</template>

<script>
import { parseCurrencyToNumber, parseLocaleDate } from "../helpers/componentHelper";
export default {
    props: ["item"],
    methods: {
        parseLocaleDate: parseLocaleDate,
        parseCurrencyToNumber: parseCurrencyToNumber
    }
}
</script>

<style>
.info-button {
    min-width: 25px !important;
    height: 25px !important;
    border-radius: 100%;
    padding: 0 !important;
}

.detail-modal {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    padding: 32px 24px;
}

.modal-headline {
    color: var(--blue-dark);
    font-size: 1.5em;
    margin: 0 0 30px;
}

@media (min-width: 1100px) {
    .v-dialog {
        margin-left: 250px;
    }
}
</style>