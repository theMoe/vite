<template>
  <div class="menu">
    <router-link :key="links[0].text" :to="links[0].href" class="logo-container">
        <div v-on:click="setActive(0)">
            <img src="../assets/logo_white_transparent.png" alt="ViteLogo"/>
            <p>VITE <span>Tools</span></p>
        </div>
    </router-link>
    <div class="navigation-container">
        <div class="button-container">
            <div v-for="(link, index) in links" v-bind:class="['btn', activeMenuItem == index ? 'active' : '']" :key="link.text" v-on:click="setActive(index)">
                <router-link v-if="index == 3" :key="link.text" :to="link.href + subMenuLinks[activeSubMenuItem]">{{ link.text }}</router-link>
                <router-link v-else :key="link.text" :to="link.href">{{ link.text }}</router-link>
            </div>
        </div>
    </div>
    <div v-on:click="toggleMenu" class="navigation-button">
        <div class="navigation-button__burger"></div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  data: () => ({
    links: [
      { text: "Dashboard", href: "/" },
      { text: "Whales", href: "/whales" },
      { text: "Wallet", href: "/wallet" },
      { text: "Downloads", href: "/downloads/" },
      { text: "Tokens", href: "/tokens" },
      { text: "SBP", href: "/sbp" },
      { text: "Full Nodes", href: "/fullnodes" },
      { text: "Transactions", href: "/transactions" },
    ],
    maxMobileWidth: 0
  }),
  computed: mapState([
    'activeMenuItem',
    'activeSubMenuItem',
    'subMenuLinks'
  ]),
  methods: {
    toggleMenu() {
      const navigation = document.getElementsByClassName("navigation-container")[0];
      const navigationBtn = document.getElementsByClassName("navigation-button")[0];
      const menu = document.getElementsByClassName("menu")[0];
      if (window.innerWidth <= this.maxMobileWidth) {
        if (navigationBtn.classList.contains("open")) {
          navigationBtn.classList.remove("open");
          navigation.classList.remove("open");
          menu.classList.remove("open");
        } else {
          navigationBtn.classList.add("open");
          navigation.classList.add("open");
          menu.classList.add("open");
        }
      }
    },
    setActive(index) {
      this.$store.commit('setActiveMenuItem', index);
      if (window.innerWidth <= this.maxMobileWidth) {
        this.toggleMenu();
      }
    }
  },
  created() {
    window.onload = () => {
      this.maxMobileWidth = parseInt(getComputedStyle(document.body).getPropertyValue("--mobile-max-width"));
      const navigationBtn = document.getElementsByClassName("navigation-button")[0];
      if (window.innerWidth <= this.maxMobileWidth && navigationBtn.classList.contains("open")) {
        this.toggleMenu();
      }
    };
  }
};
</script>

<style scoped>
.menu {
    height: 100vh;
    flex-basis: 200px;
    background: var(--blue-darkest);
    display: flex;
    flex-wrap: wrap;
    box-shadow: 1px 0 10px var(--blue-darkest);
    color: white;
    position: sticky;
    top: 0;
    z-index: 10000;
    overflow: scroll;
    -ms-overflow-style: none; 
    scrollbar-width: none;
}

.menu::-webkit-scrollbar {
    display: none;
}

.logo-container {
    flex-basis: 100%;
    height: 120px;
    margin: 0 10px;
    padding: 0 10px 0 0;
    border-bottom: 1px solid var(--blue-lightest); 
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    text-decoration: none;
    color: inherit;
}

.logo-container > div {
    display: flex;
    flex-basis: 100%;
    justify-content: center;
    align-items: center;
}

.logo-container p {
    margin: 20px 0 0 -5px;
    font-weight: 200;
    font-size: 19pt;
    letter-spacing: 2px;
    white-space: nowrap;
    display: inline-block;
    -webkit-transform: scale(1.15, 1.05);
    -moz-transform: scale(1.15, 1.05);
    -ms-transform: scale(1.15, 1.05);
    -o-transform: scale(1.15, 1.05);
    transform: scale(1.15, 1.05);
}

.logo-container p span {
    letter-spacing: 0;
}

.logo-container img {
    width: 55px;
    height: 55px;
}

.navigation-container {
    display: flex;
    justify-content: center;
    flex-basis: 100%;
    height: calc(100% - 150px);
}

.button-container {
    margin: 50px 0 0 20px;
    height: 625px;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
}

.button-container .btn {
    flex-basis: 100%;
    height: 65px;
    padding: 0 0 0 20px;
    display: flex;
    align-items: center;
    font-size: 16.5pt;
    font-weight: 200;
    border-top-left-radius: 15px; 
    border-bottom: 2px solid rgba(255, 255, 255, 0.15);
    cursor: pointer;
    transition: all .3s;
}

.button-container .btn.active {
    border-bottom: 2px solid var(--orange);
    background: var(--blue-dark);
    border-bottom-left-radius: 15px;
}

.button-container .btn:hover {
    background: var(--blue-dark);
    border-bottom-left-radius: 15px;
}

.button-container .btn a {
    flex-basis: 100%;
    height: 100%;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    text-decoration: none;
    color: inherit;
}

.navigation-button {
    position: relative;
    display: none;
    justify-content: center;
    align-items: center;
    width: 70px;
    height: 80px;
    cursor: pointer;
    transition: all 0.5s ease-in-out;
}

.navigation-button__burger {
    width: 50px;
    height: 6px;
    background: white;
    border-radius: 5px;
    transition: all 0.5s ease-in-out;
}

.navigation-button__burger::before, .navigation-button__burger::after {
    content: "";
    position: absolute;
    width: 50px;
    height: 6px;
    background: white;
    border-radius: 5px;
    transition: all 0.5s ease-in-out;
}

.navigation-button__burger::before {
    transform: translateY(-16px);
}

.navigation-button__burger::after {
    transform: translateY(16px);
}

.navigation-button.open .navigation-button__burger {
    background: transparent;
    box-shadow: none;
}

.navigation-button.open .navigation-button__burger::before {
    transform: rotate(45deg);
}

.navigation-button.open .navigation-button__burger::after {
    transform: rotate(-45deg);
}

@media (max-width: 1100px) {
    .menu {
        width: 100%;
        height: 80px;
        min-height: auto;
        flex-basis: auto;
        justify-content: space-between;
        background: none;
        transition: height .5s ease-out;
    }

    .menu.open {
        height: calc(80px + var(--nav-button-mobile-height) * (var(--nav-buttons) + 1));
    }

    .menu > * {
        background: var(--blue-darkest);        
    }

    .navigation-container {
        height: auto;
        transform: translateY(-100%);
        transition: transform .5s ease-out;
        order: 2;
    }

    .navigation-container.open {
        transform: translateY(0%);
    }

    .button-container {
        flex-basis: 90%;
    }

    .logo-container, .logo-container > div {
        justify-content: flex-start;
    }

    .logo-container {
        flex-basis: calc(100% - 70px);
        border-bottom: none;
        height: 80px;
        margin: 0;
        padding: 0 10px;
    }

    .logo-container p {
        font-size: 20pt;
    }

    .logo-container img {
        width: 60px;
        height: 60px;
    }

    .logo-container, .navigation-button {
        z-index: 2;
    }

    .button-container {
        margin: 0;
        height: calc(var(--nav-button-mobile-height) * (var(--nav-buttons) + 1));
        justify-content: space-evenly;
    }

    .button-container .btn {
        flex-basis: 100%;
        height: var(--nav-button-mobile-height);
        padding: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 15pt;
    }

    .button-container .btn:hover {
        background: var(--blue-dark);
        border-radius: 10px;
    }

    .button-container .btn.active {
        border-bottom: 2px solid var(--orange);
        background: var(--blue-dark);
        border-radius: 10px;
    }

    .button-container .btn a {
        justify-content: center;
    }

    .navigation-button {
        display: flex;
    }
}
</style>