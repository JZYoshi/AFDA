<template>
  <v-container fluid class="fill-height align-start">
    <v-row>
      <v-col cols="5">
        <v-autocomplete
          v-model="airlines_selected"
          :items="airlines"
          label="Airlines"
          outlined
          multiple
          chips
          small-chips
          dense
        ></v-autocomplete>
      </v-col>
      <v-col cols="5">
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
        v-for="fig_raw in fig_raw_list"
        :key="fig_raw.descriptor"
        xl="4"
        lg="6"
        md="12"
      >
        <v-card class="mx-auto">
          <div
            :id="'compare-fig-' + fig_raw.descriptor"
            class="fig-canvas mx-auto"
          ></div>
          <v-divider></v-divider>
          <div
            :id="'kde-entropy-fig-' + fig_raw.descriptor"
            class="fig-canvas mx-auto"
          ></div>
        </v-card>
      </v-col>
    </v-row>
    <v-overlay
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
  height: 55vh;
  width: 40vw;
}
</style>

<script>
import axios from "axios";
import Plotly from "plotly.js-dist";
import get_unit from "../../utils/my_utils";

export default {
  data() {
    return {
      loading_airlines: true,
      loading_descriptors: true,
      loading_fig: false,
      airlines: [],
      descriptors: [],
      airlines_selected: null,
      descriptors_selected: null,
      fig_raw_list: []
    };
  },
  methods: {
    compare: function() {
      this.loading_fig = true;
      axios
        .post("http://127.0.0.1:5000/compareairlines", {
          airlines: this.airlines_selected,
          descriptors: this.descriptors_selected
        })
        .then(res => {
          this.fig_raw_list = res.data;
          this.$forceUpdate();
          this.$forceNextTick(() => {
            let to_plot = this.fig_raw_list.length;
            for (const fig_data of this.fig_raw_list) {
              Plotly.react(
                "compare-fig-" + fig_data.descriptor,
                fig_data.airlines.flatMap(airline_stat => [
                  {
                    x: airline_stat.descriptor_values,
                    type: "histogram",
                    histnorm: "probability density",
                    opacity: 0.5,
                    name: airline_stat.airline
                  },
                  {
                    x: airline_stat.x_kde,
                    y: airline_stat.kde_values,
                    type: "scatter",
                    line: { dash: "dot" },
                    name: airline_stat.airline + " KDE"
                  }
                ]),
                {
                  title: {
                    text:
                      "<b>" +
                      fig_data.descriptor.replaceAll("_", " ").toUpperCase() +
                      " PDF</b>"
                  },
                  xaxis: {
                    title: {
                      text:
                        fig_data.descriptor +
                        " (" +
                        get_unit(fig_data.descriptor) +
                        ")"
                    }
                  },
                  margin: { l: 60, r: 40, t: 60, b: 40 },
                  autosize: true,
                  barmode: "overlay"
                },
                {
                  responsive: true
                }
              ).then(() => {
                to_plot = to_plot - 1;
                if (to_plot == 0) {
                  this.loading_fig = false;
                }
              });

              Plotly.react(
                "kde-entropy-fig-" + fig_data.descriptor,
                [
                  {
                    z: fig_data.kde_entropy,
                    x: fig_data.airlines.map(e => e.airline),
                    y: fig_data.airlines.map(e => e.airline),
                    type: "heatmap"
                  }
                ],
                {
                  title: { text: "KDE Distance" },
                  margin: { t: 60, b: 40 },
                  autosize: true
                },
                {
                  responsive: true
                }
              );
            }
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
      .post("http://127.0.0.1:5000/allairlines", { threshold: 3 })
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
