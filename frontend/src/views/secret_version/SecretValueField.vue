<script setup lang="ts">
import { ref } from 'vue';

const props = defineProps<{ value: string }>();

const show = ref(false);

// const generateString = (length: number) => {
// 	let result = '';
// 	const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
// 	const charactersLength = characters.length;
// 	let counter = 0;
// 	while (counter < length) {
// 		result += characters.charAt(Math.floor(Math.random() * charactersLength));
// 		counter += 1;
// 	}
// 	return result;
// };
</script>

<template>
	<v-text-field
		variant="underlined"
		:model-value="props.value"
		:append-inner-icon="show ? 'md:visibility' : 'md:visibility_off'"
		:type="show ? 'text' : 'password'"
		label="Secret value"
		counter
		@click:append-inner="show = !show"
	>
		<!-- append-icon="md:bolt" -->
		<!-- @click:append="generateString(32)" -->
	</v-text-field>
</template>
