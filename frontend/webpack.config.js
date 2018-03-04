'use strict' ;


const webpack = require('webpack') ;
const path = require('path') ;
const CopyWebpackPlugin = require('copy-webpack-plugin') ;
const CleanWebpackPlugin = require('clean-webpack-plugin') ;
const ExtractTextPlugin = require('extract-text-webpack-plugin') ;

const dist_dir = path.resolve(__dirname, 'dist') ;
const babel_presets = ['env']


module.exports = {
    entry: {
        'app' : './js/app',
        'test' : './js/test'
    },
    output: {
        path: dist_dir,
        filename: 'js/[name].js'
    },
    resolve: {
        alias: {
            vue: 'vue/dist/vue.min.js'  // by default esm runtime does not include template compiler
        }
    },
    plugins: [
        new CleanWebpackPlugin([dist_dir]),
        new CopyWebpackPlugin([
            { from: 'html/*.html', to: '.' },
            { from: 'favicon.ico', to: '.' }
        ]),
        // new ExtractTextPlugin('css/[name].css'),
        new webpack.ProvidePlugin({
            _: 'lodash',
            _map: ['lodash', 'map'],
            $: 'jquery',
            jQuery: 'jquery',
            'window.jQuery': 'jquery',
            Popper: ['popper.js', 'default']  // default es2015 export
            VuE: ['vue/dist/vue.esm.js', 'default']
        })
    ],
    module: {
        rules: [
            {
                test: /\.txt$/,
                use: {
                    loader: 'raw-loader'
                }
            },
            {
                test: /\.css$/,
                use: ExtractTextPlugin.extract({
                    fallback: 'style-loader',
                    use: 'css-loader'
                })
            },
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: babel_presets,
                        plugins: []
                    }
                }
            },
            {
                test: /.*\.(eot|woff2?|ttf|svg)(\?(#\w+&)?v=\d+\.\d+\.\d+(#\w+)?)?$/,
                use: {
                    loader: 'file-loader',
                    options: {
                        name: '[name].[ext]',
                        outputPath: 'fonts/',
                        publicPath: '../'
                    }
                }
            },
            {
                test: /\.(png|jpeg)$/,
                use: {
                    loader: 'file-loader',
                    options: {
                        name: '[path][name].[ext]',
                        outputPath: 'assets/'
                    }
                }
            },
        ]
    }
}
