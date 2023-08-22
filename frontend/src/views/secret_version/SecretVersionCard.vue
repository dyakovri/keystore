<script setup lang="ts">
import SecretValueField from './SecretValueField.vue';

const props = defineProps<{
	secretVersion: {
		id: number;
		number: number;
		description: string;
		create_ts: string;
		value: { [key: string]: string };
	};
}>();
</script>

<template>
	<v-container>
		<v-row v-for="(v, k) in props.secretVersion.value" :key="k">
			<v-col cols="5">
				<v-text-field :model-value="k" variant="underlined" label="Secret name"></v-text-field>
			</v-col>
			<v-col cols="7">
				<SecretValueField :value="v"></SecretValueField>
			</v-col>
		</v-row>
		<v-row>
			<v-btn>Сохранить изменения</v-btn>
			<v-btn color="variant">Сбросить изменения</v-btn>
		</v-row>
	</v-container>
</template>
