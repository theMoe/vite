<template>
  <div class="appbar">
    <router-link :key="links[0].text" :to="links[0].href" class="logo-container">
      <div v-on:click="setActive(0)">
        <img src="../assets/logo_black_transparent.png" alt="ViteLogo" height="70" width="70" />
        <p>VITE <span>tools</span></p>
      </div>
    </router-link>
    <div class="navigation-container">
      <div
        class="btn"
        v-for="(link, index) in links"
        :key="link.text"
        v-on:click="setActive(index)"
      >
        <router-link :key="link.text" :to="link.href">{{ link.text }}</router-link>
      </div>
    </div>
    <div v-on:click="toggleMenu" class="navigation-button">
      <div class="navigation-button__burger"></div>
    </div>
  </div>
</template>
<script>
export default {
  name: "ViteAppBar",
  data: () => ({
    links: [
      { text: "Home", href: "/" },
      { text: "Transactions", href: "/transactions" },
      // { text: "ViteX Orders", href: "/exchangeOrders" },
      { text: "Dividends", href: "/dividends" },
      { text: "Staking VITE", href: "/stakingVITE" },
      { text: "Market Making", href: "/marketMaking" },
      { text: "Trading", href: "/trading" },
      { text: "Referring", href: "/referal" },
      { text: "Contact", href: "/contact" }
    ]
  }),
  methods: {
    toggleMenu() {
      const navigation = document.getElementsByClassName(
        "navigation-container"
      )[0];
      const navigationBtn = document.getElementsByClassName(
        "navigation-button"
      )[0];
      if (window.innerWidth <= 810) {
        if (navigationBtn.classList.contains("open")) {
          navigation.style.display = "none";
          navigationBtn.classList.remove("open");
          navigation.classList.remove("open");
        } else {
          navigation.style.display = "flex";
          navigationBtn.classList.add("open");
          navigation.classList.add("open");
        }
      }
    },
    toggleResponsiveMenu() {
      const navigation = document.getElementsByClassName(
        "navigation-container"
      )[0];
      const appbar = document.getElementsByClassName("appbar")[0];
      const navigationBtn = document.getElementsByClassName(
        "navigation-button"
      )[0];
      if (window.innerWidth <= 810) {
        if (appbar.children[1] == navigation) {
          appbar.removeChild(navigation);
          appbar.appendChild(navigation);
        }
        if (
          !navigationBtn.classList.contains("open") &&
          navigation.style.display == "flex"
        ) {
          navigation.style.display = "none";
        }
      } else {
        if (appbar.children[1] == navigationBtn) {
          appbar.removeChild(navigationBtn);
          appbar.appendChild(navigationBtn);
        }
        if (navigation.style.display == "none") {
          navigation.style.display = "flex";
        }
      }
    },
    setActive(index) {
      const buttons = document.getElementsByClassName("btn");
      for (let i = 0; i < buttons.length; i++) {
        if (buttons[i].classList.contains("active") && i !== index) {
          buttons[i].classList.remove("active");
        }
        if (!buttons[i].classList.contains("active") && i === index) {
          buttons[i].classList.add("active");
        }
      }
      if (window.innerWidth <= 810) {
        this.toggleMenu();
      }
    },
    setActiveInital() {
      for (let i = 0; i < this.links.length; i++) {
        if (i !== 0 && window.location.href.indexOf(this.links[i].href) != -1) {
          this.setActive(i);
          return;
        } 
      }
      this.setActive(0);
    }
  },
  created() {
    window.onload = () => {
      this.toggleResponsiveMenu();
      this.setActiveInital();
      if (window.innerWidth <= 810) {
        this.toggleMenu();
      }
    };

    window.addEventListener("resize", () => {
      this.toggleResponsiveMenu();
    });
  }
};
</script>