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
      <h3 class="modal-headline">SBP</h3>
      <v-simple-table>
        <template v-slot:default>
          <tbody>
            <tr>
              <td>Name</td>
              <td>{{ item.sbp_name }}</td>
            </tr>
            <tr>
              <td>Block Producing Address</td>
              <td>{{ item.block_producing_address }}</td>
            </tr>
            <tr>
              <td>Block Creation Rewards</td>
              <td>{{ item.block_creation_rewards }}</td>
            </tr>
            <tr>
              <td>Votes</td>
              <td>{{ item.votes }}</td>
            </tr>
            <tr>
              <td>Count</td>
              <td>{{ item.count }}</td>
            </tr>
            <tr>
              <td>Ratio (in %)</td>
              <td>{{ item.ratio }}</td>
            </tr>
            <tr>
              <td>Total Rewards</td>
              <td>{{ item.rewards_in_total }}</td>
            </tr>
            <tr>
              <td>Rewards of Votes</td>
              <td>{{ item.rewards_of_votes }}</td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </v-card>
  </v-dialog>
</template>

<script>
import { parseLocaleDate } from "../helpers/componentHelper";
export default {
    props: ["item"],
    methods: {
        parseLocaleDate: parseLocaleDate
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