import { cutString, formatter } from '../helpers/moduleHelper.js';
import { sbpService } from '../services/sbp.service.js';

export const sbp = {
    namespaced: true,
    state: {
        error: false,
        exception: false,
        sbpTableData: {header: [], items: []},
        sbpTotalData: {},
        loading: false,
    },
    actions: {
        async getSbpList({ commit }) {
            commit("setLoading", true);
            let dataResponse;
            try {
                dataResponse = await sbpService.getSbpList();
            } catch (e) {
                commit("setException", true);
                return false;
            }
            commit("setLoading", false);
            const dataResponseJson = await dataResponse.json();
            
            if (dataResponse.status != 200) {
                commit("setError", true);
            } else {
                commit("setError", false);
                const tableData = {
                    header: [
                        {text: "🏆", value: "rank"},
                        {text: "Name", value: "sbp_name", sortable: false},
                        {text: "Address", value: "address_short", sortable: false},
                        {text: "Votes", value: "votes"},
                        {value: "details", sortable: false},
                    ], 
                    items: []
                };

                let counter = 0;
                for (const sbp of dataResponseJson) {
                    sbp.rank = ++counter;
                    sbp.details = "";
                    sbp.address_short = cutString(sbp.block_producing_address);
                    sbp.votes = formatter.format(sbp.votes);
                    sbp.block_creation_rewards = formatter.format(sbp.block_creation_rewards);
                    sbp.ratio = formatter.format(sbp.ratio);
                    sbp.rewards_in_total = formatter.format(sbp.rewards_in_total);
                    sbp.rewards_of_votes = formatter.format(sbp.rewards_of_votes);
                }

                tableData.items = dataResponseJson;

                commit('setSbpTableData', tableData);
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
        setSbpTableData(state, data) {
            state.sbpTableData = data;
        },
        setSbpTotalData(state, data) {
            state.sbpTotalData = data;
        },
    },
};
