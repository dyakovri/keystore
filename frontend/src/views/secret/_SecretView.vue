<script setup lang="ts">
import secretVersionRow from './SecretVersionRow.vue';
import secretVersionCard from '../secret_version/SecretVersionCard.vue';

const secret = {
	id: 1,
	name: 'My secret 1',
	description: 'This is very confident data with login, password and many others',
	create_ts: '2023-01-01',
	modify_ts: '2023-08-20',
	version: 3,
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
const secret_versions = [
	{
		id: 1,
		number: 1,
		description: 'Создали секрет',
		create_ts: '2023-01-01',
	},
	{
		id: 5,
		number: 2,
		description: 'Сменили пароль',
		create_ts: '2023-02-01',
	},
	{
		id: 155,
		number: 3,
		description: 'Сменили пароль',
		create_ts: '2023-08-20',
	},
].reverse();
</script>

<template>
	<v-container>
		<h2>{{ secret.name }}</h2>
		<p>{{ secret.description }}</p>
		<v-card title="Текущая версия" color="background" elevation="0">
			<secretVersionCard :secret-version="current_version"> </secretVersionCard>
		</v-card>

		<v-card title="Все версии" color="background" elevation="0">
			<v-card-text>
				<div class="font-weight-bold ms-1 mb-2">Today</div>
				<v-timeline density="compact" align="start">
					<v-timeline-item
						v-for="s in secret_versions"
						:key="s.id"
						icon="md:commit"
						dot-color="secondary"
						fill-dot
					>
						<secretVersionRow :secret-id="Number($route.params.sec_id)" :secret-version="s" />
					</v-timeline-item>
				</v-timeline>
			</v-card-text>
		</v-card>
	</v-container>
</template>
