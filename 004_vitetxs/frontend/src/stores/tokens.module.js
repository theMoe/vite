import { cutString, formatter } from '../helpers/moduleHelper.js';
import { tokensService } from '../services/tokens.service.js';

export const tokens = {
  namespaced: true,
  state: {
    error: false,
    exception: false,
    tokenTableData: {header: [], items: []},
    loading: false,
  },
  actions: {
    async getTokenData({ commit }) {
      commit("setLoading", true);
      let dataResponse;
      try {
        dataResponse = await tokensService.getTokenData();
      } catch (e) {
        commit("setException", true);
        return false;
      }
      commit("setLoading", false);
      const dataResponseJson = await dataResponse.json();
      
      if (dataResponse.status != 200) {
        commit("setError", true);
      } else {
        commit('setError', false);
        const tableData = {
            header: [
              {text: "Symbol", value: "tokenSymbol", sortable: false},
              {text: "Name", value: "tokenName", sortable: false},
              {text: "ID", value: "id_short", sortable: false},
              {text: "Supply", value: "totalSupply"},
              {text: "Owner", value: "owner", sortable: false},
              {value: "details", sortable: false}
            ], 
            items: []
        };

        for (const item of dataResponseJson) {
            item.details = "";
            item.owner_short = cutString(item.owner);
            item.id_short = cutString(item.tokenId);
            item.totalSupply = formatter.format(item.totalSupply);    

            tableData.items.push(item);
        }

        commit("setTokenTableData", tableData);
        return true;
      }
    },
    async initLoading ({ commit }) {
      commit('setException', false);
      commit('setLoading', false);
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
    setTokenTableData(state, data) {
        state.tokenTableData = data;
    }
  },
};
