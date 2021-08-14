import {
  cutString,
  getCurrentCycle,
  roundToNthDecimal,
} from '../helpers/moduleHelper.js';
import { nodesService } from '../services/nodes.service.js';

export const nodes = {
  namespaced: true,
  state: {
    error: false,
    exception: false,
    basicNodeData: [],
    nodeListData: { header: [], items: [] },
    nodeMapData: {},
    loading: {},
  },
  actions: {
    async getBasicNodeData({ commit }, cycles) {
      commit('setLoading', {
        ...this.state.nodes.loading,
        basicDataLoading: true,
      });
      let dataResponse;
      try {
        dataResponse = await nodesService.getBasicNodeData(cycles);
      } catch (e) {
        commit('setException', true);
        return false;
      }
      commit('setLoading', {
        ...this.state.nodes.loading,
        basicDataLoading: false,
      });
      const dataResponseJson = await dataResponse.json();
      if (dataResponse.status != 200) {
        commit('setError', true);
      } else {
        commit('setError', false);
        dataResponseJson.lastCount = Object.values(
          dataResponseJson.last_timespan
        );
        dataResponseJson.count = Object.values(
          dataResponseJson.current_timespan
        );
        dataResponseJson.rewardCount = [
          0,
          0,
          roundToNthDecimal(dataResponseJson.count.pop(), 2),
        ];
        dataResponseJson.lastRewardCount = [
          0,
          0,
          roundToNthDecimal(dataResponseJson.lastCount.pop(), 2),
        ];
        dataResponseJson.change = [
          roundToNthDecimal(
            dataResponseJson.count[0] - dataResponseJson.lastCount[0],
            2
          ),
          roundToNthDecimal(
            dataResponseJson.count[1] - dataResponseJson.lastCount[1],
            2
          ),
          roundToNthDecimal(
            dataResponseJson.rewardCount[2] -
              dataResponseJson.lastRewardCount[2],
            2
          ),
        ];

        commit('setBasicNodeData', dataResponseJson);
        return true;
      }
    },
    async getNodeListData({ commit }, listCycle) {
      commit('setLoading', {
        ...this.state.nodes.loading,
        listDataLoading: true,
      });
      let dataResponse;
      try {
        dataResponse = await nodesService.getNodeListData(listCycle);
      } catch (e) {
        commit('setException', true);
        return false;
      }
      commit('setLoading', {
        ...this.state.nodes.loading,
        listDataLoading: false,
      });
      const dataResponseJson = await dataResponse.json();

      if (dataResponse.status != 200) {
        commit('setError', true);
      } else {
        commit('setError', false);

        let tableData;

        if (listCycle == getCurrentCycle()) {
          tableData = {
            header: [
              { text: 'Address', value: 'address_short' },
              { text: 'Name', value: 'node_name' },
              { text: 'Status', value: 'isAlive' },
              { text: 'Online ratio (in %)', value: 'online_ratio' },
              { text: 'Version', value: 'version' },
              { text: 'IP', value: 'ip' },
            ],
            items: [],
          };
        } else {
          tableData = {
            header: [
              { text: 'Address', value: 'address_short' },
              { text: 'Name', value: 'node_name' },
              { text: 'Online ratio (in %)', value: 'online_ratio' },
              { text: 'Version', value: 'version' },
              { text: 'IP', value: 'ip' },
            ],
            items: [],
          };
        }

        for (const item of dataResponseJson) {
          item.address_short = cutString(item.address);
          item.online_ratio = roundToNthDecimal(item.online_ratio, 2);
          tableData.items.push(item);
        }

        commit('setNodeListData', tableData);
        return true;
      }
    },
    async getNodeMapData({ commit }) {
      commit('setLoading', {
        ...this.state.nodes.loading,
        nodeMapLoading: true,
      });
      let dataResponse;
      try {
        dataResponse = await nodesService.getNodeMapData();
      } catch (e) {
        commit('setException', true);
        return false;
      }
      commit('setLoading', {
        ...this.state.nodes.loading,
        nodeMapLoading: false,
      });
      const dataResponseJson = await dataResponse.json();

      if (dataResponse.status != 200) {
        commit('setError', true);
      } else {
        commit('setError', false);

        for (const node of dataResponseJson.countries) {
          if (node.value < 2) {
            node.fill = '#ffc099';
          } else if (node.value < 5) {
            node.fill = '#ff914d';
          } else if (node.value < 50) {
            node.fill = '#ff711a';
          } else if (node.value < 100) {
            node.fill = '#e65800';
          } else if (node.value < 200) {
            node.fill = '#b34400';
          } else {
            node.fill = '#662700';
          }
        }

        commit('setNodeMapData', dataResponseJson);
        return true;
      }
    },
    async initLoading({ commit }) {
      commit('setException', false);
      commit('setLoading', {
        basicDataLoading: true,
        listDataLoading: true,
        nodeMapLoading: true,
      });
    },
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
    setBasicNodeData(state, data) {
      state.basicNodeData = data;
    },
    setNodeListData(state, data) {
      state.nodeListData = data;
    },
    setNodeMapData(state, data) {
      state.nodeMapData = data;
    },
  },
};
