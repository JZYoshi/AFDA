<template>
  <v-container fluid class="fill-height align-start">
    <v-row dense>
      <v-col cols="12" class="d-flex justify-center">
        <v-btn-toggle
          class="my-3"
          color="primary"
          v-model="chosen"
          mandatory
          multiple
          rounded
          dense
          @change="load()"
        >
          <v-btn value="Metar">
            Metar
          </v-btn>
          <v-btn value="ADSB">
            Asd-b
          </v-btn>
        </v-btn-toggle>
      </v-col>
      <v-col cols="12">
        <v-card>
          <div class="d-flex flex-no-wrap justify-space-between">
            <v-col cols="6">
              <v-img :src="cah_fig_src" height="75vh" contain />
            </v-col>
            <v-col cols="6">
              <v-data-table
                :headers="airlines_headers"
                :items="airlines"
                :search="search_airline"
                item-key="airline"
                show-group-by
                height="65vh"
                fixed-header
                disable-pagination
                hide-default-footer
              >
                <template v-slot:top>
                  <v-text-field
                    v-model="search_airline"
                    label="Search for Airlines or Index..."
                    class="mx-4"
                  ></v-text-field>
                </template>
              </v-data-table>
            </v-col>
          </div>
        </v-card>
      </v-col>
      <v-col cols="12">
        <v-card>
          <div class="d-flex flex-no-wrap justify-space-between">
            <v-col cols="6">
              <v-img :src="pca_fig_src" height="75vh" contain />
            </v-col>
            <v-col cols="6">
              <v-data-table
                :headers="clustering_stats_headers"
                :items="clustering_stats"
                :search="search_group"
                item-key="airline"
                show-group-by
                height="65vh"
                fixed-header
                disable-pagination
                hide-default-footer
              >
                <template v-slot:top>
                  <v-text-field
                    v-model="search_group"
                    label="Search for Group"
                    class="mx-4"
                  ></v-text-field>
                </template>
              </v-data-table>
            </v-col>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      chosen: ["Metar", "ADSB"],
      cah_fig_src: null,
      pca_fig_src: null,
      search_airline: "",
      search_group: "",
      airlines: [],
      airlines_headers: [
        {
          text: "Index",
          value: "index",
          width: "6vw",
          align: "center",
          sortable: true,
          filterable: true,
          groupable: false,
          divider: true,
          class: "secondary white--text"
        },
        {
          text: "Airline",
          value: "airline",
          width: "20vw",
          filterable: true,
          groupable: false,
          class: "secondary white--text"
        },
        {
          text: "Group",
          value: "group",
          width: "10vw",
          align: "center",
          groupable: true,
          filterable: false,
          sortable: true,
          class: "secondary white--text"
        }
      ],
      clustering_stats: [],
      clustering_stats_headers: []
    };
  },
  mounted() {
    this.load_fig();
    this.airlines = require("../assets/clustering_res/classification.json");
    this.airlines.forEach((e, i) => {
      e.index = i;
    });
    this.load_table();
  },
  methods: {
    load_fig() {
      if (this.chosen.length == 2) {
        this.cah_fig_src = require("../assets/clustering_res/cah.svg");
        this.pca_fig_src = require("../assets/clustering_res/pca.svg");
      } else if (this.chosen[0] == "Metar") {
        this.cah_fig_src = require("../assets/clustering_res/cah_meteo.svg");
        this.pca_fig_src = require("../assets/clustering_res/pca_meteo.svg");
      } else if (this.chosen[0] == "ADSB") {
        this.cah_fig_src = require("../assets/clustering_res/cah_operation.svg");
        this.pca_fig_src = require("../assets/clustering_res/pca_operation.svg");
      }
    },
    load_table() {
      if (this.chosen.length == 2) {
        this.airlines_headers[2].value = "group";
        this.clustering_stats = require("../assets/clustering_res/clustering_stats.json");
      } else if (this.chosen[0] == "Metar") {
        this.airlines_headers[2].value = "group_meteo";
        this.clustering_stats = require("../assets/clustering_res/clustering_stats_meteo.json");
      } else if (this.chosen[0] == "ADSB") {
        this.airlines_headers[2].value = "group_operation";
        this.clustering_stats = require("../assets/clustering_res/clustering_stats_operation.json");
      }

      const labels = Object.keys(this.clustering_stats[0]);
      this.clustering_stats_headers = labels.map(k => ({
        text: k,
        value: k,
        width: (36.0 / labels.length).toString() + "vw",
        align: "center",
        sortable: true,
        groupable: false,
        class: "secondary white--text"
      }));
      this.clustering_stats.forEach((e, i) => {
        e.group = i + 1;
      });
      this.clustering_stats_headers.unshift({
        text: "Group",
        value: "group",
        width: "6vw",
        align: "center",
        groupable: false,
        sortable: true,
        class: "secondary white--text",
        divider: true
      });
    },
    load() {
      this.load_fig();
      this.load_table();
    }
  }
};
</script>
