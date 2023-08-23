<script setup lang="ts">
import secretVersionCard from '../secret_version/SecretVersionCard.vue';

const secret = {
	id: 1,
	name: 'My secret 1',
	description: 'This is very confident data with login, password and many others',
	create_ts: '2023-01-01',
	modify_ts: '2023-08-20',
	version: 2,
};
const current_version = {
	id: 155,
	number: 3,
	description: 'Сменили пароль',
	create_ts: '2023-08-20',
	value: {
		username: 'dyakovri',
		password: 'V3RY5tr0ngPASS!',
	},
};
</script>

<template>
	<v-container>
		<h2>{{ secret.name }} (версия {{ current_version.number }} от {{ current_version.create_ts }})</h2>
		<p>{{ secret.description }}</p>
		<p>Причина изменения: {{ current_version.description }}</p>
		<v-card title="Текущая версия" color="background" elevation="0">
			<secretVersionCard :secret-version="current_version" :readonly="current_version.number != secret.version">
			</secretVersionCard>
		</v-card>
	</v-container>
</template>
