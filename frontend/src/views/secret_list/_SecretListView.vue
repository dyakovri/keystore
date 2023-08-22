<script setup lang="ts">
import secretRow from './SecretRow.vue';
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
	</v-container>
</template>
