import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home
  },
  {
    path: "/stats",
    name: "Stats",
    component: () => import("../views/Stats.vue"),
    children: [
      {
        path: "general",
        name: "General",
        component: () => import("../components/stats/General.vue")
      },
      {
        path: "airlines",
        component: {
          render: c => c("router-view")
        },
        children: [
          {
            path: "airline/:id",
            name: "AirlineStat",
            component: () => import("../components/stats/AirlineStat.vue")
          },
          {
            path: "",
            name: "Airlines",
            component: () => import("../components/stats/AirlineShowCase.vue")
          },
          {
            path: "*",
            component: () => import("../components/stats/AirlineShowCase.vue")
          }
        ]
      },
      {
        path: "compare",
        name: "Compare",
        component: () => import("../components/stats/Compare.vue")
      },
      {
        path: "",
        redirect: "general"
      },
      {
        path: "*",
        redirect: "general"
      }
    ]
  },
  {
    path: "/clustering",
    name: "Clustering",
    component: () => import("../views/Clustering.vue")
  }
];

const router = new VueRouter({
  routes
});

export default router;
