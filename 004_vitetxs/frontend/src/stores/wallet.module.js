import { walletService } from "../services/wallet.service.js";
import dayjs from "dayjs";
import { currencyFormatter, cutString, formatter, getCurrentCycle, parseDate, roundToNthDecimal, tokenFormatter } from "../helpers/moduleHelper.js";

export const wallet = {
  namespaced: true,
  state: {
    error: false,
    exception: false,
    basicData: {},
    nodeListData: {header: [], items: []},
    transactionListData: {header: [], items: []},
    tokenListData: {header: [], items: []},
    tokenGraphData: [],
    loading: {},
  },
  actions: {
    async getBasicWalletData({ commit }, viteAddress) {
      commit("setLoading", {
        ...this.state.wallet.loading,
        basicDataLoading: true,
      });

      let dataResponse;
      try {      
        dataResponse = await walletService.getBasicWalletData(viteAddress);
      } catch (e) {
        commit("setException", true);
        return false;
      }
      
      commit("setLoading", {
        ...this.state.wallet.loading,
        basicDataLoading: false,
      });
      const dataResponseJson = await dataResponse.json();

      if (dataResponse.status != 200) {
        commit("setError", true);
      } else {
        const parsedData = {
          viteBalance: formatter.format(dataResponseJson.viteBalance),
          quota: formatter.format(dataResponseJson.quota),
          stakedVite: formatter.format(dataResponseJson.stakedVite)
        };
        commit("setError", false);
        commit("setBasicData", parsedData);
      }
    },
    async getNodeListData({ commit }, { viteAddress, cycle }) {
      commit("setLoading", {
        ...this.state.wallet.loading,
        nodeListLoading: true,
      });
      
      let dataResponse;
      try {      
        dataResponse = await walletService.getNodesByViteAddress(viteAddress, cycle);
      } catch (e) {
        commit("setException", true);
        return false;
      }

      commit("setLoading", {
        ...this.state.wallet.loading,
        nodeListLoading: false,
      });
      const dataResponseJson = await dataResponse.json();
      if (dataResponse.status != 200) {
        commit("setError", true);
      } else {
        commit("setError", false);

        let tableData;

        if (cycle === getCurrentCycle()) {
          tableData = {
              header: [
                  {text: "Name", value: "name"},
                  {text: "Status", value: "status"},
                  {text: "Online ratio (in %)", value: "online_ratio"},
                  {text: "Version", value: "version"},
                  {text: "IP", value: "ip"},
              ], 
              items: []
          };
        } else {
          tableData = {
              header: [
                  {text: "Name", value: "name"},
                  {text: "Online ratio (in %)", value: "online_ratio"},
                  {text: "Version", value: "version"},
                  {text: "IP", value: "ip"},
              ], 
              items: []
          }; 
        }
        
        for (const item of dataResponseJson) {
          item.online_ratio = roundToNthDecimal(item.online_ratio, 2);
          tableData.items.push(item);
          item.block_height = formatter.format(item.block_height);
        }

        commit("setNodeListData", tableData);
      }
    },
    async getTransactionListData({ commit }, viteAddress) {
      commit("setLoading", {
        ...this.state.wallet.loading,
        transactionListLoading: true,
      });
      
      let dataResponse;
      try {      
        dataResponse = await walletService.getTransactionListData(viteAddress);
      } catch (e) {
        commit("setException", true);
        return false;
      }

      commit("setLoading", {
        ...this.state.wallet.loading,
        transactionListLoading: false,
      });
      const dataResponseJson = await dataResponse.json();
      if (dataResponse.status != 200) {
        commit("setError", true);
      } else {
        commit("setError", false);
        const tableData = {
          header: [
            { text: "Date", value: "date" },
            { text: "Symbol", value: "symbol" },
            { text: "Amount", value: "amount_normalised" },
            { text: "From", value: "from_address_short" },
            { text: "To", value: "to_address_short" },
            { text: "", value: "details", sortable: false },
          ],
          items: [],
        };

        for (const item of dataResponseJson) {
          item.created_at = parseDate(item.created_at);
          item.date = dayjs(item.created_at).format("YYYY-MM-DD");
          item.from_address_short = cutString(item.from_address);
          item.to_address_short = cutString(item.to_address);
          item.amount_normalised = formatter.format(item.amount_normalised);
          item.details = "";

          tableData.items.push(item);
        }

        commit("setTransactionListData", tableData);
      }
    },
    async getTokenData({ commit }, viteAddress) {
      commit("setLoading", {
        ...this.state.wallet.loading,
        tokenDataLoading: true,
      });
      let dataResponse;
      try {      
        dataResponse = await walletService.getTokenData(viteAddress);
      } catch (e) {
        commit("setException", true);
        return false;
      }
      commit("setLoading", {
        ...this.state.wallet.loading,
        tokenDataLoading: false,
      });
      const dataResponseJson = await dataResponse.json();

      if (dataResponse.status != 200) {
        commit("setError", true);
      } else {
        const graphBackgroundColors = [
          "#e66312",
          "#1272e6",
          "#BC8034",
          "#70A288",
          "#FFEE93",
          "#9191E9",
          "#870058",
        ];

        const graphData = {
          symbols: dataResponseJson.map((token) => token.symbol),
          usdt_value: dataResponseJson.map((token) => token.usdt_value),
          background: graphBackgroundColors,
        };

        for (let index = 0; index <= graphData.symbols.length; index++) {
          graphData.background.push(
            "#" + Math.floor(Math.random() * 16777215).toString(16)
          );
        }

        commit("setTokenGraphData", graphData);

        const tableData = {
          header: [
            { text: "Symbol", value: "symbol" },
            { text: "Amount", value: "amount" },
            { text: "Value (USD)", value: "usdt_value" },
          ],
          items: [],
        };

        for (const item of dataResponseJson) {
          item.usdt_value = currencyFormatter.format(item.usdt_value);
          item.amount = tokenFormatter.format(item.amount);

          tableData.items.push(item);
        }

        commit("setTokenListData", tableData);
      }
      return true;
    },
    async initLoading({ commit }) {
      commit('setException', false);
      commit('setLoading', {
        basicDataLoading: true,
        nodeListLoading: true,
        transactionListLoading: true,
        tokenDataLoading: true,
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
    setBasicData(state, value) {
      state.basicData = value;
    },
    setNodeListData(state, value) {
      state.nodeListData = value;
    },
    setTransactionListData(state, value) {
      state.transactionListData = value;
    },
    setTokenListData(state, value) {
      state.tokenListData = value;
    },
    setTokenGraphData(state, value) {
      state.tokenGraphData = value;
    },
  },
};
