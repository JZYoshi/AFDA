<template>
  <v-navigation-drawer app permanent expand-on-hover clipped>
    <v-list nav dense>
      <v-list-item to="/stats/general">
        <v-list-item-icon>
          <v-icon>mdi-information</v-icon>
        </v-list-item-icon>
        <v-list-item-title>General Information</v-list-item-title>
      </v-list-item>
      <v-list-item to="/stats/airlines">
        <v-list-item-icon>
          <v-icon>mdi-airplane</v-icon>
        </v-list-item-icon>
        <v-list-item-title>Airline Companies</v-list-item-title>
      </v-list-item>
      <v-list-item to="/stats/compare">
        <v-list-item-icon>
          <v-icon>mdi-compare-horizontal</v-icon>
        </v-list-item-icon>
        <v-list-item-title>Compare Airlines</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>
