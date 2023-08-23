import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
	{
		path: '/',
		redirect: '/sec',
	},
	{
		path: '/sec',
		component: () => import('@/views/secret_list/_SecretListView.vue'),
		meta: { isSecure: true },
	},
	{
		path: '/sec/create',
		component: () => import('@/views/secret_create/_SecretCreateView.vue'),
		meta: { isSecure: true },
	},
	{
		path: '/sec/:sec_id(\\d+)',
		component: () => import('@/views/secret/_SecretView.vue'),
		props: true,
		meta: { isSecure: true },
	},
	{
		path: '/sec/:sec_id(\\d+)/ver/:ver_id(\\d+)',
		component: () => import('@/views/secret_version/_SecretVersionView.vue'),
		props: true,
		meta: { isSecure: true },
	},
	{
		path: '/auth',
		component: () => import('@/views/auth/_AuthView.vue'),
		props: true,
	},
	{
		path: '/:(.*)',
		redirect: '/sec',
	},
];

export const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes,
});

router.beforeEach(async to => {
	// Заменяем токен на новый из хэш-параметров
	if (to.hash.startsWith('#token=')) {
		localStorage.setItem('token', to.hash.substring(7));
		return { path: to.path, query: to.query, hash: undefined };
	}

	// Проверяем что есть токен в localStorage для секьюрных ручек
	if (to.meta.isSecure && (localStorage.getItem('token') || '') == '') {
		return { path: '/auth' };
	}
});
