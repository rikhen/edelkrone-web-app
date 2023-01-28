module.exports = {
  outputDir: 'www',
  assetsDir: 'assets',
  productionSourceMap: false,
  configureWebpack: {
    performance: {
      hints: false
    }
  },
  devServer: {
    host: 'youthful-bohr.37-120-190-180.plesk.page'
  }
}
