<template>
  <v-container fluid class="fill-height">
    <v-row justify="space-around">
      <v-col
        v-for="(fig_raw, i) in fig_raw_list"
        :key="i"
        xl="3"
        lg="4"
        md="6"
        sm="12"
      >
        <div class="fig-canvas mx-auto" :id="'airline-stat-' + i" />
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
.fig-canvas {
  height: 320px;
  width: 400px;
}
</style>
<script>
import axios from "axios";
import $mpld3 from "../../utils/mpld3API";

export default {
  data() {
    return {
      fig_raw_list: [],
      loading: true
    };
  },
  mounted() {
    axios
      .post("http://127.0.0.1:5000/airlinestat", {
        airline: this.$route.params.id
      })
      .then(res => {
        this.fig_raw_list = res.data.fig_raw_list;
        this.$forceUpdate();
        this.$forceNextTick(() => {
          for (let i = 0; i < this.fig_raw_list.length; i++) {
            $mpld3.draw_figure("airline-stat-" + i, this.fig_raw_list[i]);
          }
          this.loading = false;
        });
      })
      .catch(err => {
        console.error(err);
      });
  }
};
</script>
