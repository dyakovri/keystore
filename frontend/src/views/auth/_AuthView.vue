<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const token = ref('');

const save = () => {
	console.log(token.value);

	localStorage.setItem('token', token.value);
	router.push('/sec');
};
</script>

<template>
	<v-container>
		<v-row>
			<h1>Вы не вошли в систему!</h1>
		</v-row>
		<v-row>
			<p>Войдите с использованием корпоративного приложения или вставьте докен доступа ниже</p>
		</v-row>
		<v-row>
			<v-divider class="my-6"></v-divider>
		</v-row>
		<v-row>
			<v-text-field
				v-model="token"
				label="Токен пользователя"
				type="input"
				hint="Введите токен вашего пользователя для доступа в систему"
			></v-text-field>
		</v-row>
		<v-row>
			<v-btn @click="save()">Сохранить</v-btn>
		</v-row>
	</v-container>
</template>
