import { downloadFileFromResponse } from '../helpers/moduleHelper.js';
import { exchangeOrdersService } from '../services/exchangeOrders.service.js';

export const exchangeOrders = {
    namespaced: true,
    state: {
        loading: false,
        error: false,
    },
    actions: {
        async getMultiselectData({ commit }) {
            const dataResponse = await exchangeOrdersService.getMultiselectData();
            const dataResponseJson = await dataResponse.json();
            if (dataResponse.status != 200) {
                commit("setError", true);
            } else {
                commit("setError", false);
                return dataResponseJson;
            }
        },
        async getStatistics({ commit }, {viteAddress, params}) {
            commit('setLoading', true);
            let statisticResponse;
            try {
                statisticResponse = await exchangeOrdersService.getStatistics(viteAddress, params);
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
                downloadFileFromResponse(`orders_${viteAddress}.csv`, blob);
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
