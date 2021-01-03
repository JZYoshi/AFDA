<template>
  <v-container fluid class="fill-height">
    <v-row align="center" justify="center">
      <v-col cols="5">
        <v-row justify="center">
          <v-col offset="3">
            <h2>
              Number of Airlines: <span class="nb">{{ nb_airlines }}</span>
            </h2>
          </v-col>
        </v-row>
        <v-row justify="center">
          <v-col offset="3">
            <h2>
              Number of Flights: <span class="nb">{{ nb_flights }}</span>
            </h2>
          </v-col>
        </v-row>
      </v-col>
      <v-col cols="7">
        <div id="general-info-fig"></div>
      </v-col>
    </v-row>
    <v-overlay
      absolute
      :value="loading"
      opacity="1"
      color="background"
      z-index="1"
    >
      <v-progress-circular
        :size="70"
        :width="7"
        color="secondary"
        indeterminate
      ></v-progress-circular>
    </v-overlay>
  </v-container>
</template>

<style scoped>
#general-info-fig {
  width: 800px;
  height: 600px;
}

.nb {
  color: var(--v-accent-base);
}
</style>

<script>
import axios from "axios";
import $mpld3 from "../../utils/mpld3API";

export default {
  data: function() {
    return {
      loading: true,
      nb_airlines: null,
      nb_flights: null
    };
  },
  methods: {},
  mounted() {
    axios
      .get("http://127.0.0.1:5000/generalinfo")
      .then(res => {
        this.nb_airlines = res.data.nb_airlines;
        this.nb_flights = res.data.tt_flights;
        $mpld3.draw_figure("general-info-fig", res.data.fig_raw);
        this.loading = false;
      })
      .catch(err => {
        console.error(err);
      });
  }
};
</script>
