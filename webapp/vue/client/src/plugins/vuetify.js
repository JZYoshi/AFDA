import Vue from "vue";
import Vuetify from "vuetify/lib/framework";
import colors from "vuetify/lib/util/colors";

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    options: {
      customProperties: true
    },
    themes: {
      light: {
        primary: colors.blue.darken2,
        secondary: colors.red.lighten2,
        accent: colors.deepOrange.darken3,
        background: colors.grey.lighten3
      },
      dark: {
        primary: colors.blue.darken2,
        secondary: colors.red.lighten2,
        accent: colors.deepOrange.darken3,
        background: colors.grey.lighten3
      }
    }
  }
});
