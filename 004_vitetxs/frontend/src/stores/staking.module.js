import { downloadFileFromResponse } from '../helpers/moduleHelper.js';
import { stakingService } from '../services/staking.service.js';

export const staking = {
  namespaced: true,
  state: {
    loading: false,
    error: false,
  },
  actions: {
    async getStatistics({ commit }, viteAddress) {
      commit("setLoading", true);
      let statisticResponse;
      try {
        statisticResponse = await stakingService.getStatistics(viteAddress);
      } catch (e) {
        commit('setLoading', false);
        commit('setError', true);
        return;
      }
      commit("setLoading", false);
      if (statisticResponse.status != 200) {
        commit("setError", true);
      } else {
        commit('setError', false);
        const blob = await statisticResponse.blob();
        downloadFileFromResponse(`staking_${viteAddress}.csv`, blob);
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
  }
};
