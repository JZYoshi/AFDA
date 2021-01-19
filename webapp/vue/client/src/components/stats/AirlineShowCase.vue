<template>
  <v-container fluid class="fill-height">
    <v-row>
      <v-col
        v-for="id in Object.keys(flights_numbers)"
        :key="id"
        xl="2"
        lg="3"
        md="4"
        sm="6"
      >
        <AirlineCard
          class="mx-auto"
          :airline-id="id"
          :airline-avail-flights="flights_numbers[id] || 0"
        />
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
<script>
import axios from "axios";
export default {
  data() {
    return {
      flights_numbers: {},
      loading: true
    };
  },
  computed: {},
  mounted() {
    axios
      .get("http://127.0.0.1:5000/flightsnumbers")
      .then(res => {
        this.flights_numbers = res.data;
        this.loading = false;
      })
      .catch(err => {
        console.error(err);
      });
  }
};
</script>
