import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import vuetify from "./plugins/vuetify";
import LoadScript from "vue-plugin-load-script";
import StatsNavBar from "./components/stats/StatsNavBar.vue";
import AirlineCard from "./components/stats/AirlineCard.vue";
import "./assets/global.css";
import VueForceNextTick from "vue-force-next-tick";

Vue.config.productionTip = false;
Vue.use(LoadScript);
Vue.use(VueForceNextTick);
Vue.loadScript("/static/js/d3.v5.min.js").then(() => {
  Vue.loadScript("/static/js/mpld3.v0.5.2.js");
});

Vue.component("StatsNavBar", StatsNavBar);
Vue.component("AirlineCard", AirlineCard);

new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount("#app");
