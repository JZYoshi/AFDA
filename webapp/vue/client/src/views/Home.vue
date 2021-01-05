<template>
  <v-container>
    <v-row class="text-center">
      <v-col cols="12">
        <v-img
          :src="require('../assets/logo.svg')"
          class="my-3"
          contain
          height="200"
        />
      </v-col>

      <v-col class="mb-2">
        <h1 class="display-2 font-weight-bold mb-3">
          Welcome to AFDA
        </h1>

        <p class="subheading font-weight-regular">
          A Platform for <b>A</b>irline <b>F</b>light <b>D</b>ata
          <b>A</b>nalysis
          <br />
          Developped by a group of students of ISAE-SUPAERO
        </p>
      </v-col>

      <v-col class="mb-5" cols="12">
        <h2 class="headline font-weight-bold mb-5">
          Ready to start?
        </h2>

        <v-row justify="center">
          <v-btn class="mx-3" color="primary" to="/stats"
            >Statistic Results</v-btn
          >
          <v-btn class="mx-3" color="primary" to="/clustering"
            >Airline Clustering</v-btn
          >
        </v-row>
      </v-col>

      <v-col class="mb-5" cols="12">
        <h2 class="headline font-weight-bold mb-3">
          Get to the source code
        </h2>

        <v-row justify="center">
          <a
            href="https://github.com/JZYoshi/AFDA"
            class="subheading mx-3"
            target="_blank"
          >
            GitHub
          </a>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "HelloWorld"
};
</script>
