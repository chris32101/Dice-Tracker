import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/home.vue";
import SignUp from "../views/auth/sign-up.vue";
import Login from "../views/auth/login.vue";
import Dashboard_Home from "../views/dashboard/home.vue";
import League_Home from "../views/dashboard/league/home.vue";
import League_Create from "../views/dashboard/league/create.vue";
import League_Join from "../views/dashboard/league/join.vue";
import League_Preview from "../views/dashboard/league/onGoingLeague/preview.vue";
import League_CreateTeams from "../views/dashboard/league/onGoingLeague/createTeams.vue";
import League_Bracket from "../views/dashboard/league/onGoingLeague/bracket.vue";
import League_Leaderboard from "../views/dashboard/league/onGoingLeague/leaderboard.vue";
import League_StatTracker from "../views/dashboard/league/onGoingLeague/statTracker.vue";
import Profile from "../views/dashboard/profile/profile.vue";
import PageNotFound from "../views/404.vue";

Vue.use(VueRouter);

const routes = [
  {
    // location
    path: "/",
    // what we want to call it
    name: "Home",
    // component that is utilized
    component: Home,
    meta: {
      // do you need to be logged in to the website
      requiresAuth: false,
      // prevent user from accessing webpage is logged in
      disableRouteIfLoggedIn: false,
    },
  },
];

const router = new VueRouter({
  mode: "history",
  base: import.meta.env.BASE_URL,
  routes,
});

export default router;
