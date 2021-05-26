const path = require('path');

module.exports = {
    mode: "development",

    // entry point is where Webpack will find the start of our React app and bundle from there.
    entry: path.resolve(__dirname, 'frontend_react/src/index.js'),

     // to allow use of Async/await in our components. 
     entry: ['babel-polyfill', path.resolve(__dirname, 'frontend_react/src/index.js')],
     
    output: {
        // options related to how webpack emits results

        // where compiled files go
        path: path.resolve(__dirname, "frontend_react/static/frontend/public/"),

        // 127.0.0.1/static/frontend/public/ where files are served from
        publicPath: "/static/frontend/public/",
        filename: 'main.js',  // the same one we import in index.html
    },
    module: {
        // configuration regarding modules
        rules: [
            {
                // regex test for js and jsx files
                test: /\.(js|jsx)?$/,
                // don't look in the node_modules/ folder
                exclude: /node_modules/,
                // for matching files, use the babel-loader
                use: {
                    loader: "babel-loader",
                    options: {presets: ["@babel/env"]}
                },
            }
        ],
    },
};