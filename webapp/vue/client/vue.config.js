module.exports = {
  transpileDependencies: ["vuetify"],
  assetsDir: "static",
  chainWebpack: config => {
    config.module.rule('eslint').use('eslint-loader').options({
      fix: true
    })
  }
};
