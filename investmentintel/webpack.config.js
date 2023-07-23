const path = require('path');

module.exports = {
  entry: './fundsintel/static/fundsintel/index/App.js',
  output: {
    path: path.resolve(__dirname, './fundsintel/static/fundsintel/js'), // Change this path to your desired output directory for JavaScript files
    filename: 'bundle.js',
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-react'],
          },
        },
      },
    ],
  },
};
