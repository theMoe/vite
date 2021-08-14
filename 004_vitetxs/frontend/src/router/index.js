import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '../store'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue'),
    beforeEnter: (to, from, next) => {
      store.commit('setActiveMenuItem', 0);
      next();
    }
  },
  {
    path: '/whales',
    name: 'Whales',
    component: () => import('../views/Whales.vue'),
    beforeEnter: (to, from, next) => {
      store.commit('setActiveMenuItem', 1);
      next();
    }
  },
  {
    path: '/wallet',
    name: 'Wallet',
    component: () => import('../views/Wallet.vue'),
    beforeEnter: (to, from, next) => {
      store.commit('setActiveMenuItem', 2);
      next();
    }
  },
  {
    path: '/downloads',
    name: 'Downloads',
    beforeEnter: (to, from, next) => {
      store.commit('setActiveMenuItem', 3);
      next();
    },
    component: () => import('../views/Downloads.vue'),
    children: [
      {
        path: 'transactions',
        component: () => import('../views/downloads/Transactions.vue'),
        beforeEnter: (to, from, next) => {
          store.commit('setActiveSubMenuItem', 0);
          next();
        }
      },
      {
        path: 'exchangeOrders',
        component: () => import('../views/downloads/ExchangeOrders.vue'),
        beforeEnter: (to, from, next) => {
          store.commit('setActiveSubMenuItem', 1);
          next();
        }
      },
      {
        path: 'priceHistory',
        component: () => import('../views/downloads/Prices.vue'),
        beforeEnter: (to, from, next) => {
          store.commit('setActiveSubMenuItem', 2);
          next();
        }
      },
      {
        path: 'dividends',
        component: () => import('../views/downloads/Dividends.vue'),
        beforeEnter: (to, from, next) => {
          store.commit('setActiveSubMenuItem', 3);
          next();
        }
      },
      {
        path: 'stakingVITE',
        component: () => import('../views/downloads/StakingVite.vue'),
        beforeEnter: (to, from, next) => {
          store.commit('setActiveSubMenuItem', 4);
          next();
        }
      },
      {
        path: 'marketMaking',
        component: () => import('../views/downloads/MarketMaking.vue'),
        beforeEnter: (to, from, next) => {
          store.commit('setActiveSubMenuItem', 5);
          next();
        }
      },
      {
        path: 'trading',
        component: () => import('../views/downloads/Trading.vue'),
        beforeEnter: (to, from, next) => {
          store.commit('setActiveSubMenuItem', 6);
          next();
        }
      },
      {
        path: 'referal',
        component: () => import('../views/downloads/Referring.vue'),
        beforeEnter: (to, from, next) => {
          store.commit('setActiveSubMenuItem', 7);
          next();
        }
      },
    ]
  },
  {
    path: '/tokens',
    name: 'Tokens',
    component: () => import('../views/Tokens.vue'),
    beforeEnter: (to, from, next) => {
      store.commit('setActiveMenuItem', 4);
      next();
    }
  },
  {
    path: '/sbp',
    name: 'SBP',
    component: () => import('../views/Sbp.vue'),
    beforeEnter: (to, from, next) => {
      store.commit('setActiveMenuItem', 5);
      next();
    }
  },
  {
    path: '/fullnodes',
    name: 'Full Nodes',
    component: () => import('../views/Nodes.vue'),
    beforeEnter: (to, from, next) => {
      store.commit('setActiveMenuItem', 6);
      next();
    }
  },
  {
    path: '/transactions',
    name: 'Transactions',
    component: () => import('../views/Transactions.vue'),
    beforeEnter: (to, from, next) => {
      store.commit('setActiveMenuItem', 7);
      next();
    }
  },
]

const router = new VueRouter({
  routes: routes
})

export default router
