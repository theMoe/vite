import { cutString, downloadFileFromResponse, formatter, getDelayString, parseDate } from '../helpers/moduleHelper.js';
import { transactionsService } from '../services/transactions.service.js';

export const transactions = {
    namespaced: true,
    state: {
        loading: {
            downloadLoading: false,
            listLoading: false
        },
        error: true,
        exception: true,
        currentTransactionsTableData: {header: [], items: []},
    },
    actions: {
        async getStatistics({ commit }, {viteAddress, params}) {
            commit('setLoading', {...this.state.loading, downloadLoading: true});
            let statisticResponse;
            try {
                statisticResponse = await transactionsService.getStatistics(viteAddress, params);
            } catch (e) {
                commit('setLoading', false);
                commit('setError', true);
                return;
            }
            commit('setLoading', {...this.state.loading, downloadLoading: false});
            if (statisticResponse.status != 200) {
                commit("setError", true);
            } else {
                commit("setError", false);
                const blob = await statisticResponse.blob();
                downloadFileFromResponse(`transactions_${viteAddress}.csv`, blob);
            }
        },
        async getCurrentTransactionsList({ commit }) {
            commit('setLoading', {...this.state.loading, listLoading: true});
            let dataResponse;
            try {
                dataResponse = await transactionsService.getCurrentTransactionListData();
            } catch (e) {
                commit("setException", true);
                return false;
            }
            commit('setLoading', {...this.state.loading, listLoading: false});
            const dataResponseJson = await dataResponse.json();
            if (dataResponse.status != 200) {
                commit("setError", true);
            } else {
                commit('setError', false);
                const tableData = {
                    header: [
                        {text: "Hash", value: "tx_hash_short", sortable: false},
                        {text: "Token", value: "symbol", sortable: false},
                        {text: "Amount", value: "amount_normalised"},
                        {text: "From", value: "from_address_short"},
                        {text: "To", value: "to_address_short"},
                        {text: "Age", value: "age"},
                        {text: "", value: "details", sortable: false}
                    ], 
                    items: []
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

                commit('setCurrentTransactionsTableData', tableData);
            }
        },
        async initLoading ({ commit }) {
            commit('setException', false);
            commit('setLoading', {
              downloadLoading: true,
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
        setCurrentTransactionsTableData(state, data) {
            state.currentTransactionsTableData = data;
        },
    },
};
