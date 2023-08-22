import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
	{
		path: '/',
		redirect: '/secret',
	},
	{
		path: '/secret',
		component: () => import('@/views/secret_list/_SecretListView.vue'),
	},
	{
		path: '/secret/:sec_id(\\d+)',
		component: () => import('@/views/secret/_SecretView.vue'),
	},
	{
		path: '/secret/:sec_id(\\d+)/ver/:ver_id(\\d+)',
		component: () => import('@/views/secret_version/_SecretVersionView.vue'),
	},
];

export const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes,
});
