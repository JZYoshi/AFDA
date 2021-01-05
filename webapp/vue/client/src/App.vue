<template>
  <v-app>
    <v-app-bar app clipped-left color="primary" dark>
      <div class="d-flex align-center">
        <v-img
          class="shrink mr-2"
          contain
          :src="require('./assets/logo.svg')"
          transition="scale-transition"
          width="40"
        />

        <span>AFDA</span>
      </div>

      <v-spacer></v-spacer>

      <v-btn text to="/" class="mr-2">
        Home
      </v-btn>

      <v-btn text to="/stats" class="mr-2">
        Stats
      </v-btn>

      <v-btn text to="/clustering" class="mr-2">
        Clustering
      </v-btn>
    </v-app-bar>

    <StatsNavBar v-if="$route.path.startsWith('/stats')" />

    <v-main>
      <v-container fluid class="fill-height">
        <router-view></router-view>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: "App",

  methods: {}
};
</script>
