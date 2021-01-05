<template>
  <v-container fluid class="fill-height">
    <v-row justify="space-around">
      <v-col
        v-for="(fig_raw, i) in fig_data_list"
        :key="i"
        xl="3"
        lg="4"
        md="6"
        sm="12"
      >
        <div class="fig-canvas mx-auto" :id="'airline-stat-' + i" />
      </v-col>
    </v-row>
    <v-overlay :value="loading" opacity="1" color="background" z-index="1">
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
.fig-canvas {
  height: 320px;
  width: 400px;
}
</style>
<script>
import axios from "axios";
import Plotly from "plotly.js-dist";

export default {
  data() {
    return {
      fig_data_list: [],
      loading: true
    };
  },
  mounted() {
    axios
      .post("http://127.0.0.1:5000/airlinestat", {
        airline: this.$route.params.id
      })
      .then(res => {
        this.fig_data_list = res.data;
        this.$forceUpdate();
        this.$forceNextTick(() => {
          let to_plot = this.fig_data_list.length;
          for (let i = 0; i < this.fig_data_list.length; i++) {
            Plotly.newPlot(
              "airline-stat-" + i,
              [
                {
                  x: this.fig_data_list[i].values,
                  type: "histogram",
                  histnorm: "probability density"
                }
              ],
              {
                title: { text: this.fig_data_list[i].label },
                margin: { l: 60, r: 40, t: 60, b: 40 }
              }
            ).then(() => {
              to_plot = to_plot - 1;
              if (to_plot == 0) {
                this.loading = false;
              }
            });
          }
        });
      })
      .catch(err => {
        console.error(err);
      });
  }
};
</script>
