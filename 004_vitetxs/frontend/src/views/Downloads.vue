<template>
  <div class="content-container" id="download">
    <div class="submenu">
        <div v-for="(link, index) in links" v-bind:class="['btn', activeSubMenuItem == index ? 'active' : '']" :key="link.text" v-on:click="setActive(index)">
            <router-link :key="link.text" :to="link.href">{{ link.text }}</router-link>
        </div>
    </div>
    <div class="card">
        <router-view/>
    </div>
    <contact-footer/>
  </div>
</template>

<script>
import ContactFooter from '../components/ContactFooter.vue';
export default {
  components: { ContactFooter },
    data: () => ({
        links: [
        { text: "Transactions", href: "/downloads/transactions" },
        { text: "ViteX Orders", href: "/downloads/exchangeOrders" },
        { text: "ViteX Prices", href: "/downloads/priceHistory" },
        { text: "Dividends", href: "/downloads/dividends" },
        { text: "Staking VITE", href: "/downloads/stakingVITE" },
        { text: "Market Making", href: "/downloads/marketMaking" },
        { text: "Trading", href: "/downloads/trading" },
        { text: "Referring", href: "/downloads/referal" }
        ]
    }),
    computed: {
        activeSubMenuItem () {
            return this.$store.state.activeSubMenuItem;
        }
    },
    methods: {
        setActive(index) {
            this.$store.commit('setActiveSubMenuItem', index);
            if (window.innerWidth <= this.maxMobileWidth) {
                this.toggleMenu();
            }
        }
    }
}
</script>

<style>
.submenu {
    flex-basis: 100%;
    padding: 30px;
    min-height: 80px;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
}

.submenu .btn {
    border-radius: 25px;
    background: white;
    box-shadow: 1px 1px 5px var(--blue-dark);
    height: 65px;
    width: 140px;
    margin: 5px 10px;
    padding: 0 2px;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    transition: all .5s;
}

.submenu .btn:hover, .submenu .btn:active {
    background: var(--orange-lightest);
}

.submenu .btn.active {
    background: var(--orange);
    box-shadow: 1px 1px 5px var(--orange-dark);
    color: white;
}

.submenu a {
    text-decoration: none;
    color: var(--blue);
    font-size: 14pt;
    flex-basis: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    transition: all .5s;
}

.submenu .btn.active a {
    color: white;
}

@media (max-width: 1100px) {
    .submenu {
        justify-content: center;
    }
}

@media (max-width: 700px) {
    .submenu {
        padding: 10px;
    }

    .submenu .btn {
        height: 50px;
        width: 110px;
        margin: 10px;
        padding: 0 2px;
    }

    .submenu .btn a {
        font-size: 10.5pt;
    }
}
</style>