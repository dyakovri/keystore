<script setup lang="ts">
import secretRow from './SecretRow.vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const secrets = [
	{ id: 1, name: 'My secret 1', description: 'This is very confident data with login, password and many others' },
	{ id: 2, name: 'My secret 2', description: 'This is very confident data with login, password and many others' },
	{ id: 3, name: 'My secret 3', description: 'This is very confident data with login, password and many others' },
];
</script>

<template>
	<v-container>
		<v-list lines="two" select-strategy="classic">
			<v-list-subheader>Все доступные секреты</v-list-subheader>

			<secretRow v-for="s in secrets" :key="s.id" :secret="s"></secretRow>
		</v-list>

		<v-layout-item model-value position="bottom" class="text-end" size="88">
			<div class="ma-4">
				<v-btn icon="md:add" size="large" color="primary" elevation="8" @click="router.push('/sec/create')" />
			</div>
		</v-layout-item>
	</v-container>
</template>
