const path = require('path');

module.exports = {
  mode: "production",
  entry: './theme/static/js/index.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'output/theme/js'),
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader']
      }
    ]
  },
  performance: {
    maxEntrypointSize: 1024000,
    maxAssetSize: 512000
  },
};
