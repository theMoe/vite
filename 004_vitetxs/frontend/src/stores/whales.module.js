import { whalesService } from '../services/whales.service.js';
import dayjs from "dayjs";
import { currencyNoFractionFormatter, cutString, formatter, parseDate } from '../helpers/moduleHelper.js';

export const whales = {
  namespaced: true,
  state: {
    error: false,
    exception: false,
    currentWhaleData: {header: [], items: []},
    topWhaleData: {header: [], items: []},
    basicWhaleData: [],
    addressWhaleData: {header: [], items: []},
    weekdayWhaleData: [],
    whalesPerWeekData: [],
    loading: {},
  },
  actions: {
    async getCurrentWhaleData({ commit }) {
      commit('setLoading', {...this.state.whales.loading, currentWhaleLoading: true});
      const dataResponse = await whalesService.getCurrentWhaleData();
      commit('setLoading', {...this.state.whales.loading, currentWhaleLoading: false});
      const dataResponseJson = await dataResponse.json();
      
      if (dataResponse.status != 200) {
        commit("setError", true);
      } else {
        commit('setError', false);
        const tableData = {
          header: [
            {text: "Date", value: "date"},
            {text: "Symbol", value: "symbol"},
            {text: "Amount", value: "amount_normalised"},
            {text: "Value (USD)", value: "transaction_in_usdt"},
            {text: "From", value: "from_address_short", sortable: false},
            {text: "To", value: "to_address_short", sortable: false},
            {value: "category", sortable: false},
            {value: "tweet", sortable: false},
            {value: "details", sortable: false}
          ], 
          items: []
        };

        for (const item of dataResponseJson) {
          item.details = "";
          item.created_at = parseDate(item.created_at);
          item.date = dayjs(item.created_at).format("YYYY-MM-DD");
          item.from_address_short = cutString(item.from_address);
          item.to_address_short = cutString(item.to_address);

          let category = "🐠";
          if (item.transaction_in_usdt > 500000) {
            category = "🐳"
          }
          else if (item.transaction_in_usdt > 100000) {
            category = "🐬";
          }
          item.category = category;
          
          item.tweet = "🐦";
          
          item.tweet_link = `https://twitter.com/vitetools/status/${item.tweet_id}`

          item.transaction_in_usdt = currencyNoFractionFormatter.format(item.transaction_in_usdt);
          item.amount_normalised = formatter.format(item.amount_normalised);

          tableData.items.push(item);
        }

        tableData.items.sort((a,b) => (a.created_at < b.created_at) ? 1 : ((b.created_at < a.created_at) ? -1 : 0))

        commit('setCurrentWhaleData', tableData);
      }
    },
    async getTopWhaleData({ commit }) {
      commit('setLoading', {...this.state.whales.loading, topWhaleLoading: true});
      const dataResponse = await whalesService.getTopWhaleData();
      commit('setLoading', {...this.state.whales.loading, topWhaleLoading: false});
      const dataResponseJson = await dataResponse.json();
      
      if (dataResponse.status != 200) {
        commit("setError", true);
      } else {
        commit('setError', false);
        const tableData = {
          header: [
            {text: "🏆", value: "rank", sortable: false},
            {text: "Date", value: "date", sortable: false},
            {text: "Symbol", value: "symbol", sortable: false},
            {text: "Amount", value: "amount_normalised", sortable: false},
            {text: "Value (USD)", value: "transaction_in_usdt", sortable: false},
            {text: "From", value: "from_address_short", sortable: false},
            {text: "To", value: "to_address_short", sortable: false},
            {value: "tweet", sortable: false},
            {value: "details", sortable: false}
          ], 
          items: []
        };

        dataResponseJson.sort((a,b) => (a.transaction_in_usdt < b.transaction_in_usdt) ? 1 : ((b.transaction_in_usdt < a.transaction_in_usdt) ? -1 : 0));

        let counter = 1;
        for (const item of dataResponseJson) {
          item.details = "";
          item.rank = counter++;

          item.created_at = parseDate(item.created_at);
          item.date = dayjs(item.created_at).format("YYYY-MM-DD");
          item.from_address_short = cutString(item.from_address);
          item.to_address_short = cutString(item.to_address);

          item.tweet = "🐦";

          item.tweet_link = `https://twitter.com/vitetools/status/${item.tweet_id}`

          item.transaction_in_usdt = currencyNoFractionFormatter.format(item.transaction_in_usdt);
          item.amount_normalised = formatter.format(item.amount_normalised);

          tableData.items.push(item);
        }

        commit('setTopWhaleData', tableData);
      }
    },
    async getBasicWhaleData({ commit }, days) {
      commit('setLoading', {...this.state.whales.loading, baseWhaleLoading: true});
      let dataResponse;
      try {
        dataResponse = await whalesService.getBasicWhaleData(days);
      } catch (e) {
        commit("setException", true); 
        return false;
      }
      commit('setLoading', {...this.state.whales.loading, baseWhaleLoading: false});
      const dataResponseJson = await dataResponse.json();
     
      if (dataResponse.status != 200) {
        commit("setError", true);
      } else {
        commit('setError', false);

        dataResponseJson.current = (dataResponseJson.current).reverse();
        dataResponseJson.previous = (dataResponseJson.previous).reverse();
        
        const change = [0, 0, 0];
        for (const i in dataResponseJson.current) {
          change[i] = dataResponseJson.current[i] - dataResponseJson.previous[i];
        }
      
        dataResponseJson.change = change;

        commit('setBasicWhaleData', dataResponseJson);
      }
      return true;
    },
    async getAddressWhaleData({ commit }) {
      commit('setLoading', {...this.state.whales.loading, addressWhaleLoading: true});
      const dataResponse = await whalesService.getAddressWhaleData();
      commit('setLoading', {...this.state.whales.loading, addressWhaleLoading: false});
      const dataResponseJson = await dataResponse.json();
      
      if (dataResponse.status != 200) {
        commit("setError", true);
      } else {
        commit('setError', false);
        const tableData = {
          header: [
            {text: "🏆", value: "rank", sortable: false},
            {text: "Summarized Value (USD)", value: "sum_usdt_value", sortable: false},
            {text: "Address", value: "address_short", sortable: false},
            {text: "Received Whales", value: "received_string", sortable: false},
            {text: "Sent Whales", value: "sent_string", sortable: false},
          ], 
          items: []
        };

        dataResponseJson.sort((a,b) => (a.sum_usdt_value < b.sum_usdt_value) ? 1 : ((b.sum_usdt_value < a.sum_usdt_value) ? -1 : 0));

        let counter = 1;
        for (const item of dataResponseJson) {
          item.rank = counter++;
          item.address_short = cutString(item.address);
          item.sum_usdt_value = currencyNoFractionFormatter.format(item.sum_usdt_value);

          item.received_string = 
            "🐳 " + item.received.count.large + "\n"
            + "🐬 " + item.received.count.medium + "\n"
            + "🐠 " + item.received.count.small + "\n";

          item.sent_string = 
            "🐳 " + item.sent.count.large + "\n"
            + "🐬 " + item.sent.count.medium + "\n"
            + "🐠 " + item.sent.count.small + "\n";

          tableData.items.push(item);
        }

        commit('setAddressWhaleData', tableData);
      }
    },
    async getWeekdayWhaleData({ commit }) {
      commit('setLoading', {...this.state.whales.loading, weekdayWhaleLoading: true});
      let dataResponse;
      try {
        dataResponse = await whalesService.getWeekdayWhaleData();
      } catch (e) {
        commit("setException", true);
        return false;
      }
      commit('setLoading', {...this.state.whales.loading, weekdayWhaleLoading: false});
      const dataResponseJson = await dataResponse.json();
      
      if (dataResponse.status != 200) {
        commit("setError", true);
      } else {
        commit('setError', false);
        commit('setWeekdayWhaleData', dataResponseJson);
      }
      return true;
    },
    async getWhalesPerWeekData({ commit }) {
      commit('setLoading', {...this.state.whales.loading, whalesPerWeekLoading: true});
      let dataResponse;
      try {
        dataResponse = await whalesService.getWhalesPerWeekData();
      } catch (e) {
        commit("setException", true); 
        return false;
      }
      commit('setLoading', {...this.state.whales.loading, whalesPerWeekLoading: false});
      const dataResponseJson = await dataResponse.json();
      
      if (dataResponse.status != 200) {
        commit("setError", true);
      } else {
        commit('setError', false);
        const parsedData = {
          cw: dataResponseJson.map(a => a.calendar_week),
          count: {
            small: dataResponseJson.map(a => a.whale_transactions.small),
            medium: dataResponseJson.map(a => a.whale_transactions.medium),
            large: dataResponseJson.map(a => a.whale_transactions.large),
          }
        }

        commit('setWhalesPerWeekData', parsedData);
      }
      return true;
    },
    async initLoading({ commit }) {
      commit('setException', false);
      commit('setLoading', {
        currentWhaleLoading: true,
        topWhaleLoading: true,
        baseWhaleLoading: true,
        addressWhaleLoading: true,
        weekdayWhaleLoading: true,
        whalesPerWeekLoading: true,
      })
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
    setCurrentWhaleData(state, data) {
        state.currentWhaleData = data;
    },
    setTopWhaleData(state, data) {
        state.topWhaleData = data;
    },
    setBasicWhaleData(state, data) {
        state.basicWhaleData = data;
    },
    setAddressWhaleData(state, data) {
        state.addressWhaleData = data;
    },
    setWeekdayWhaleData(state, data) {
        state.weekdayWhaleData = data;
    },
    setWhalesPerWeekData(state, data) {
        state.whalesPerWeekData = data;
    },
  },
};
