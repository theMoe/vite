import { downloadFileFromResponse } from '../helpers/moduleHelper.js';
import { pricesService } from '../services/prices.service.js';

export const prices = {
    namespaced: true,
    state: {
        loading: false,
        error: false,
    },
    actions: {
        async getStatistics({ commit }, params) {
            commit('setLoading', true);
            let statisticResponse;
            try {
                statisticResponse = await pricesService.getStatistics(params);
            } catch (e) {
                commit('setLoading', false);
                commit('setError', true);
                return;
            }
            commit('setLoading', false);
            if (statisticResponse.status != 200) {
                commit("setError", true);
            } else {
                commit("setError", false);
                const blob = await statisticResponse.blob();
                downloadFileFromResponse("prices.csv", blob);
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
