<script setup lang="ts">
import { ref, Ref } from 'vue';
import secretVersionCard from '../secret_version/SecretVersionCard.vue';

const name = ref('');
const description = ref('');
const current_version: Ref<{
	id: number;
	number: number;
	description: string;
	create_ts: string;
	value: { [key: string]: string };
}> = ref({ id: 0, number: 0, description: '', create_ts: '', value: {} });
</script>

<template>
	<v-container>
		<v-text-field :model-value="name"></v-text-field>
		<v-text-field :model-value="description"></v-text-field>
		<secretVersionCard :secret-version="current_version" @save="version => console.log(version)">
		</secretVersionCard>
	</v-container>
</template>
