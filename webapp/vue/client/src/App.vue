<template>
  <v-app>
    <v-app-bar app clipped-left color="primary" dark>
      <div class="d-flex align-center">
        <v-img
          alt="Vuetify Logo"
          class="shrink mr-2"
          contain
          src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"
          transition="scale-transition"
          width="40"
        />

        <span>AFDA</span>
      </div>

      <v-spacer></v-spacer>

      <v-btn text to="/stats">
        <span class="mr-2">Stats</span>
      </v-btn>

      <v-btn text to="/clustering">
        <span class="mr-2">Clustering</span>
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
