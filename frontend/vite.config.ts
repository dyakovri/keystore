import { defineConfig } from 'vite';
import { fileURLToPath, URL } from 'url';
import Stylelint from 'vite-plugin-stylelint';
import Eslint from 'vite-plugin-eslint';
import Vue from '@vitejs/plugin-vue';
import path from 'path';
import postcssPresetEnv from 'postcss-preset-env';
import vuetify from 'vite-plugin-vuetify';

// https://vitejs.dev/config/
export default defineConfig({
	css: {
		postcss: {
			plugins: [
				postcssPresetEnv({
					features: {
						'nesting-rules': true,
					},
				}),
			],
		},
	},
	plugins: [
		Vue(),
		vuetify(),
		Eslint(),
		Stylelint({
			files: [path.resolve(__dirname, 'src/**/*.{vue,css}')],
		}),
	],
	resolve: {
		alias: [{ find: '@', replacement: fileURLToPath(new URL('./src', import.meta.url)) }],
	},
	publicDir: 'src/public',
});
