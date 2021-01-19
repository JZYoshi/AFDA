<template>
  <v-container fluid class="fill-height">
    <v-row align="center" justify="center">
      <v-col cols="5">
        <v-row justify="center">
          <v-col offset="2">
            <h2>
              The flights are operated by <span class="nb">A320 family</span>
            </h2>
          </v-col>
        </v-row>
        <v-row justify="center">
          <v-col offset="2">
            <h2>
              Number of Airlines: <span class="nb">{{ nb_airlines }}</span>
            </h2>
          </v-col>
        </v-row>
        <v-row justify="center">
          <v-col offset="2">
            <h2>
              Number of Flights: <span class="nb">{{ nb_flights }}</span>
            </h2>
          </v-col>
        </v-row>
        <v-row justify="center">
          <v-col offset="2">
            <h2>
              The data are collected from <span class="nb">..</span> to
              <span class="nb">..</span>
            </h2>
          </v-col>
        </v-row>
        <v-row justify="center">
          <v-col offset="2">
            <h2>
              Other info...
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
  width: 53vw;
  height: 80vh;
}

.nb {
  color: var(--v-accent-base);
}
</style>

<script>
import axios from "axios";
import Plotly from "plotly.js-dist";

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
      .get("http://127.0.0.1:5000/flightsnumbers")
      .then(res => {
        const flights_numbers = res.data;
        this.nb_airlines = Object.keys(flights_numbers).length;
        this.nb_flights = Object.values(flights_numbers).reduce(
          (a, b) => a + b
        );
        const fig_data = [
          {
            x: Object.keys(flights_numbers),
            y: Object.values(flights_numbers),
            type: "bar"
          }
        ];
        Plotly.newPlot(
          "general-info-fig",
          fig_data,
          {
            autosize: true
          },
          {
            responsive: true
          }
        ).then(() => {
          this.loading = false;
        });
      })
      .catch(err => {
        console.error(err);
      });
  }
};
</script>
