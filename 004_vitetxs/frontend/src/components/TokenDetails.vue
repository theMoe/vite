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
      <h3 class="modal-headline">Token</h3>
      <v-simple-table>
        <template v-slot:default>
          <tbody>
            <tr>
              <td>Token ID</td>
              <td>{{ item.tokenId }}</td>
            </tr>
            <tr>
              <td>Name</td>
              <td>{{ item.tokenName }}</td>
            </tr>
            <tr>
              <td>Symbol</td>
              <td>{{ item.tokenSymbol }}</td>
            </tr>
            <tr>
              <td>Total Supply</td>
              <td>{{ item.totalSupply }}</td>
            </tr>
            <tr>
              <td>Owner</td>
              <td>{{ item.owner }}</td>
            </tr>
            <tr>
              <td>Reissuable</td>
              <td>{{ item.isReIssuable ? "Yes" : "No" }}</td>
            </tr>
            <tr>
              <td>Owner Burn Only</td>
              <td>{{ item.isOwnerBurnOnly ? "Yes" : "No" }}</td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
    props: ["item"]
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