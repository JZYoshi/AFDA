<template>
  <v-container fluid class="fill-height align-start">
    <v-row>
      <v-col cols="3">
        <v-autocomplete
          v-model="airline_1"
          :items="airlines"
          label="Airline 1"
          outlined
          dense
        ></v-autocomplete>
      </v-col>
      <v-col cols="3">
        <v-autocomplete
          v-model="airline_2"
          :items="airlines"
          label="Airline 2"
          outlined
          dense
        ></v-autocomplete>
      </v-col>
      <v-col cols="4">
        <v-autocomplete
          v-model="descriptors_selected"
          :items="descriptors"
          label="Descriptor"
          outlined
          multiple
          chips
          small-chips
          dense
        ></v-autocomplete>
      </v-col>
      <v-col cols="2" class="d-flex justify-center">
        <v-btn @click="compare()" color="primary">Compare</v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col
        v-for="(fig_raw, i) in fig_raw_list"
        :key="i"
        xl="4"
        lg="6"
        md="12"
      >
        <div :id="'compare-fig-' + i" class="fig-canvas mx-auto"></div>
      </v-col>
    </v-row>
    <v-overlay
      absolute
      :value="loading_airlines || loading_descriptors || loading_fig"
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
  height: 480px;
  width: 640px;
}
</style>

<script>
import axios from "axios";
import $mpld3 from "../../utils/mpld3API";

export default {
  data() {
    return {
      loading_airlines: true,
      loading_descriptors: true,
      loading_fig: false,
      airlines: [],
      descriptors: [],
      airline_1: null,
      airline_2: null,
      descriptors_selected: null,
      fig_raw_list: []
    };
  },
  methods: {
    compare: function() {
      this.loading_fig = true;
      axios
        .post("http://127.0.0.1:5000/compareairlines", {
          airline_1: this.airline_1,
          airline_2: this.airline_2,
          descriptors: this.descriptors_selected
        })
        .then(res => {
          this.fig_raw_list = res.data.fig_raw_list;
          this.$forceUpdate();
          this.$forceNextTick(() => {
            for (let i = 0; i < this.fig_raw_list.length; i++) {
              $mpld3.draw_figure("compare-fig-" + i, this.fig_raw_list[i]);
            }
            this.loading_fig = false;
          });
        });
    }
  },
  mounted() {
    axios
      .get("http://127.0.0.1:5000/descriptors")
      .then(res => {
        this.descriptors = res.data.descriptors;
        this.loading_descriptors = false;
      })
      .catch(err => {
        console.error(err);
      });
    axios
      .get("http://127.0.0.1:5000/allairlines")
      .then(res => {
        this.airlines = res.data.airlines;
        this.loading_airlines = false;
      })
      .catch(err => {
        console.error(err);
      });
  }
};
</script>
