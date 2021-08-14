import { downloadFileFromResponse } from '../helpers/moduleHelper.js';
import { tradingService } from '../services/trading.service.js';

export const trading = {
  namespaced: true,
  state: {
    loading: false,
    error: false,
  },
  actions: {
    async getStatistics({ commit }, viteAddress) {
      commit('setLoading', true);
      let statisticResponse;
      try {
        statisticResponse = await tradingService.getStatistics(viteAddress);
      } catch (e) {
        commit('setLoading', false);
        commit('setError', true);
        return;
      }
      commit('setLoading', false);
      if (statisticResponse.status != 200) {
        commit("setError", true);
      } else {
        commit('setError', false);
        const blob = await statisticResponse.blob();
        downloadFileFromResponse(`tradeMining_${viteAddress}.csv`, blob);
      }
    },
  },
  mutations: {
    setLoading(state, value) {
      state.loading = value;
    },
    setError(state, value) {
      state.error = value;
    },
  },
};
