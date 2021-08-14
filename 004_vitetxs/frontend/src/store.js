import Vue from 'vue';
import VueX from 'vuex';
import createPersistedState from 'vuex-persistedstate';
import { trading } from './stores/trading.module';
import { dividends } from './stores/dividends.module';
import { staking } from './stores/staking.module';
import { referring } from './stores/referring.module';
import { markets } from './stores/markets.module';
import { exchangeOrders } from './stores/exchangeOrders.module';
import { prices } from './stores/prices.module';
import { transactions } from './stores/transactions.module';
import { dashboard } from './stores/dashboard.module';
import { whales } from './stores/whales.module';
import { tokens } from './stores/tokens.module';
import { sbp } from './stores/sbp.module';
import { nodes } from './stores/nodes.module';
import { wallet } from './stores/wallet.module';

Vue.use(VueX);

const store = new VueX.Store({
  modules: {
    trading,
    dividends,
    staking,
    referring,
    markets,
    exchangeOrders,
    prices,
    transactions,
    dashboard,
    whales,
    tokens,
    sbp,
    nodes,
    wallet
  },
  state: {
    activeMenuItem: 0,
    activeSubMenuItem: 0,
    subMenuLinks: [
      'transactions',
      'exchangeOrders',
      'priceHistory',
      'dividends',
      'stakingVITE',
      'marketMaking',
      'trading',
      'referal',
    ],
    globalViteAddress: ""
  },
  mutations: {
    setActiveMenuItem(state, n) {
      state.activeMenuItem = n;
    },
    setActiveSubMenuItem(state, n) {
      state.activeSubMenuItem = n;
    },
    setGlobalViteAddress(state, n) {
      state.globalViteAddress = n;
    }
  },
  plugins: [createPersistedState()],
});

export default store;
