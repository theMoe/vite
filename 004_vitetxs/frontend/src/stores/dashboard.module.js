import { dashboardService } from "../services/dashboard.service.js";
import dayjs from "dayjs";
import { currencySmallFormatter, cutString, formatter, getDelayString, parseDate, roundToNthDecimal } from "../helpers/moduleHelper.js";

export const dashboard = {
  namespaced: true,
  state: {
    error: false,
    exception: false,
    rewardGraphData: [],
    transactionListData: {header: [], items: []},
    counts: {},
    loading: {},
  },
  actions: {
    async getRewardGraphData({ commit }) {
      commit("setLoading", { ...this.state.dashboard.loading, rewardLoading: true });
      let dataResponse;
      try {
        dataResponse = await dashboardService.getRewardGraphData();
      } catch (e) {
        commit("setException", true);
        return false;
      }
      commit("setLoading", { ...this.state.dashboard.loading, rewardLoading: false });
      const dataResponseJson = (await dataResponse.json()).reverse();
      const parsedData = { dates: [], amount: [], usdt_values: [] };

      if (dataResponse.status != 200) {
        commit("setError", true);
      } else {
        commit("setError", false);
        for (const reward of dataResponseJson) {
          parsedData.dates.push(dayjs(reward.created_at).format("MM/DD"));
          parsedData.amount.push(
            roundToNthDecimal(reward.amount_normalised, 2)
          );
          parsedData.usdt_values.push(
            roundToNthDecimal(reward.transaction_in_usdt, 2)
          );
        }
        commit("setRewardGraphData", parsedData);
        return true;
      }
    },
    async getDashboardCounts({ commit }) {
      commit("setLoading", { ...this.state.dashboard.loading, countsLoading: true });
      let dataResponse;
      try {
        dataResponse = await dashboardService.getDashboardCounts();
      } catch (e) {
        commit("setException", true);
        return false;
      }
      commit("setLoading", { ...this.state.dashboard.loading, countsLoading: false });
      const dataResponseJson = await dataResponse.json();

      if (dataResponse.status != 200) {
        commit("setError", true);
      } else {
        commit("setError", false);

        const parsedData = {
          block_height: formatter.format(dataResponseJson.block_height),
          price: currencySmallFormatter.format(roundToNthDecimal(dataResponseJson.price, 5)),
          tokens: formatter.format(dataResponseJson.tokens),
          total_accounts: formatter.format(dataResponseJson.total_accounts),
          transactions_last_day: formatter.format(dataResponseJson.transactions_last_day),
          online_nodes: formatter.format(dataResponseJson.online_nodes),
          super_nodes: formatter.format(dataResponseJson.super_nodes),
          total_supply: formatter.format(dataResponseJson.total_supply),
        }

        commit("setCounts", parsedData);
        return true;
      }
    },
    async getLastTransactions({ commit }, count) {
      commit("setLoading", { ...this.state.dashboard.loading, listLoading: true });
      let dataResponse;
      try {
        dataResponse = await dashboardService.getLastTransactions(count);
      } catch (e) {
        commit("setException", true);
        return false;
      }
      commit("setLoading", { ...this.state.dashboard.loading, listLoading: false });
      const dataResponseJson = await dataResponse.json();

      if (dataResponse.status != 200) {
        commit("setError", true);
      } else {
        commit("setError", false);
        const tableData = {
          header: [
            { text: "Hash", value: "tx_hash_short", sortable: false },
            { text: "Token", value: "symbol", sortable: false },
            { text: "Amount", value: "amount_normalised" },
            { text: "From", value: "from_address_short" },
            { text: "To", value: "to_address_short" },
            { text: "Age", value: "age" },
            { text: "", value: "details", sortable: false },
          ],
          items: [],
        };

        for (const transaction of dataResponseJson) {
          transaction.from_address_short = cutString(transaction.from_address);
          transaction.to_address_short = cutString(transaction.to_address);
          transaction.tx_hash_short = cutString(transaction.tx_hash);
          transaction.amount_normalised = formatter.format(transaction.amount_normalised);
          transaction.created_at = parseDate(transaction.created_at);
          transaction.age = getDelayString(new Date(transaction.created_at).getTime());
          transaction.details = "";
        }

        tableData.items = dataResponseJson;

        commit("setTransactionListData", tableData);
        return true;
      }
    },
    async initLoading({ commit }) {
      commit('setException', false);
      commit('setLoading', {
        countsLoading: true,
        rewardLoading: true,
        listLoading: true
      });
    }
  },
  mutations: {
    setLoading(state, value) {
      state.loading = value;
    },
    setError(state, value) {
      state.error = value;
    },
    setException(state, value) {
      state.exception = value;
    },
    setRewardGraphData(state, data) {
      state.rewardGraphData = data;
    },
    setTransactionListData(state, data) {
      state.transactionListData = data;
    },
    setCounts(state, data) {
      state.counts = data;
    },
  },
};
