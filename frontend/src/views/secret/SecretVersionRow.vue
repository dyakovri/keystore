<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter();
const props = defineProps<{
	secretId: number;
	secretVersion: {
		id: number;
		number: number;
		description: string;
		create_ts: string;
	};
}>();
</script>

<template>
	<v-list-item @click="router.push(`/sec/${props.secretId}/ver/${props.secretVersion.id}`)">
		<v-list-item-title> {{ props.secretVersion.number }}. {{ props.secretVersion.description }} </v-list-item-title>

		<v-list-item-subtitle>
			id: {{ props.secretVersion.id }} &bull; created at {{ props.secretVersion.create_ts }}
		</v-list-item-subtitle>
	</v-list-item>
</template>
