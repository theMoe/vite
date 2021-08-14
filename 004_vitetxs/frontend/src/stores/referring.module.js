import { downloadFileFromResponse } from '../helpers/moduleHelper.js';
import { referringService } from '../services/referring.service.js';

export const referring = {
  namespaced: true,
  state: {
    loading: false,
    downloadReady: false,
    error: false,
  },
  actions: {
    async getStatistics({ commit }, viteAddress) {
      commit('setLoading', true);
      let statisticResponse;
      try {
        statisticResponse = await referringService.getStatistics(viteAddress);
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
        downloadFileFromResponse(`referring_${viteAddress}.csv`, blob);
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
