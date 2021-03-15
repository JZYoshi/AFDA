<template>
  <v-hover>
    <template v-slot:default="{ hover }">
      <v-card max-width="320">
        <v-img
          :src="get_airline_img"
          :aspect-ratio="16 / 10"
          width="17vw"
          class="mx-auto"
          contain
        ></v-img>

        <v-card-text>
          <h2 class="title primary--text">
            {{ get_airline_name }}
          </h2>
          ......
        </v-card-text>

        <v-card-title>
          <p>
            Available Flights:
            <span class="accent--text">{{ airlineAvailFlights }}</span>
          </p>
        </v-card-title>

        <v-fade-transition>
          <v-overlay v-if="hover" absolute color="background" z-index="1">
            <v-btn :to="'/stats/airlines/airline/' + airlineId"
              >View Descriptors</v-btn
            >
          </v-overlay>
        </v-fade-transition>
      </v-card>
    </template>
  </v-hover>
</template>

<script>
import airline_profiles from "../../utils/airline_profiles";
export default {
  props: ["airlineId", "airlineAvailFlights"],
  computed: {
    get_airline_name: function() {
      return airline_profiles[this.airlineId]?.name || this.airlineId;
    },

    get_airline_img: function() {
      const fname = airline_profiles[this.airlineId]?.img || "wildcard.jpg";
      return require("../../assets/airline_img/" + fname);
    }
  }
};
</script>
