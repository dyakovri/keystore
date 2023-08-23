<script setup lang="ts">
import { ref, Ref } from 'vue';

defineEmits(['save']);
const props = withDefaults(
	defineProps<{
		secretVersion: {
			value: { [key: string]: string };
		};
		readonly?: boolean;
	}>(),
	{
		readonly: false,
		secretVersion: () => ({
			value: {},
		}),
	},
);

const value: Ref<{ key: string; value: string; show: boolean }[]> = ref([]);

const reset = () => {
	value.value = Object.keys(props.secretVersion.value).map(k => {
		return { key: k, value: props.secretVersion.value[k], show: false };
	});
	value.value.sort((a, b) => {
		return a.key == b.key ? 0 : a.key > b.key ? 1 : -1;
	});
};
reset();

const changeKey = (key: number, new_: string) => (value.value[key].key = new_);
const changeValue = (key: number, new_: string) => (value.value[key].value = new_);
const dropKey = (key: number) => value.value.splice(key, 1);
const createKey = () => value.value.push({ key: '', value: '', show: false });

const copyContent = async (text: string) => {
	try {
		await navigator.clipboard.writeText(text);
		console.log('Content copied to clipboard');
	} catch (err) {
		alert(`Failed to copy: ${err}`);
	}
};

const generateString = (length: number) => {
	let result = '';
	const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789,.!@#$%^&*()<>{}`~[]';
	const charactersLength = characters.length;
	let counter = 0;
	while (counter < length) {
		result += characters.charAt(Math.floor(Math.random() * charactersLength));
		counter += 1;
	}
	return result;
};
</script>

<template>
	<v-container>
		<v-row v-for="(val, key) in value" :key="key">
			<v-form style="width: 100%">
				<v-row justify="space-between">
					<v-col cols="3">
						<v-text-field
							:model-value="value[key].key"
							variant="underlined"
							label="Secret name"
							:readonly="readonly"
							@change.stop="(event: any) => changeKey(key, event.target.value)"
						>
						</v-text-field>
					</v-col>
					<v-col>
						<v-text-field
							variant="underlined"
							:model-value="value[key].value"
							:type="value[key].show ? 'text' : 'password'"
							label="Secret value"
							counter
							autocomplete="off"
							:readonly="readonly"
							@change.stop="(event: any) => changeValue(key, event.target.value)"
						>
						</v-text-field>
						<v-tooltip :text="!value[key].show ? 'Показать значение' : 'Скрыть значение'" location="bottom"
							><template #activator="{ props: isActive }">
								<v-btn
									v-bind="isActive"
									:icon="!value[key].show ? 'md:visibility' : 'md:visibility_off'"
									variant="flat"
									color="white"
									@click="value[key].show = !value[key].show"
								>
								</v-btn> </template
						></v-tooltip>
						<v-tooltip text="Копировать значение" location="bottom"
							><template #activator="{ props: isActive }">
								<v-btn
									v-bind="isActive"
									icon="md:content_copy"
									variant="flat"
									color="white"
									@click="copyContent(value[key].value)"
								>
								</v-btn> </template
						></v-tooltip>
						<v-tooltip v-if="!readonly" text="Сгенерировать случайное значение" location="bottom"
							><template #activator="{ props: isActive }">
								<v-btn
									v-if="!readonly"
									v-bind="isActive"
									icon="md:bolt"
									variant="flat"
									color="white"
									@click="value[key].value = generateString(32)"
								>
								</v-btn> </template
						></v-tooltip>
						<v-tooltip v-if="!readonly" text="Удалить поле" location="bottom"
							><template #activator="{ props: isActive }">
								<v-btn
									v-if="!readonly"
									v-bind="isActive"
									icon="md:delete"
									variant="flat"
									color="white"
									@click="dropKey(key)"
								>
								</v-btn> </template
						></v-tooltip>
					</v-col>
				</v-row>
			</v-form>
		</v-row>
		<v-row v-if="!readonly" justify="end" align="center">
			<v-btn icon="add" variant="flat" color="white" style="place-self: start start" @click="createKey()"></v-btn>
			<v-col />
			<v-btn class="mx-2" color="variant" @click="reset()">Сбросить изменения</v-btn>
			<v-btn class="mx-2" @click="$emit('save', value)">Сохранить изменения</v-btn>
		</v-row>
	</v-container>
</template>

<style scoped>
.v-col {
	display: flex;
	flex-wrap: nowrap;
}
</style>
