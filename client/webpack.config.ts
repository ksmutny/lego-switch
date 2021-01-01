import * as path from 'path'
import * as webpack from 'webpack'

export default function(env): webpack.Configuration {
    return {
        context: path.join(__dirname, 'src'),

        entry: './app.tsx',

        output: {
            path: path.join(__dirname, 'www'),
            filename: 'app.js'
        },

        devtool: 'source-map',

        externals: {
            'react': 'React',
            'react-dom': 'ReactDOM'
        },

        resolve: {
            extensions: ['.ts', '.tsx', '.js', '.jsx']
        },

        module: {
            rules: [
                {
                    test: /\.tsx?$/,
                    loader: 'ts-loader',
                    exclude: /node_modules/
                }
            ]
        }
    }
}
