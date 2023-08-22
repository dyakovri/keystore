<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter();
const props = defineProps<{
	secret: {
		isActive: boolean;
		id: number;
		name: string;
		description: string;
	};
}>();
</script>

<template>
	<v-list-item @click="router.push(`/sec/${props.secret.id}`)">
		<template #prepend>
			<v-avatar color="grey-lighten-1">
				<v-icon color="white">md:key</v-icon>
			</v-avatar>
		</template>
		<v-list-item-title>{{ props.secret.name }}</v-list-item-title>

		<v-list-item-subtitle>{{ props.secret.description }}</v-list-item-subtitle>
	</v-list-item>
</template>
