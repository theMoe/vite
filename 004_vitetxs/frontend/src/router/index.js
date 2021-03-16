import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/transactions',
    name: 'Transactions',
    component: () => import('../views/Transactions.vue')
  },
  {
    path: '/exchangeOrders',
    name: 'ExchangeOrders',
    component: () => import('../views/ExchangeOrders.vue')
  },
  {
    path: '/dividends',
    name: 'Dividends',
    component: () => import('../views/Dividends.vue')
  },
  {
    path: '/stakingVITE',
    name: 'Mining/StakingVITE',
    component: () => import('../views/StakingVite.vue')
  },
  {
    path: '/marketMaking',
    name: 'Mining/MarketMaking',
    component: () => import('../views/MarketMaking.vue')
  },
  {
    path: '/trading',
    name: 'Mining/Trading',
    component: () => import('../views/Trading.vue')
  },
  {
    path: '/referal',
    name: 'Mining/Referal',
    component: () => import('../views/Referal.vue')
  },
  {
    path: '/contact',
    name: 'Contact',
    component: () => import('../views/Contact.vue')
  }
]

const router = new VueRouter({
  routes
})

export default router
