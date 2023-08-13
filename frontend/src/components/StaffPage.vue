<script setup lang="ts">
// Родительский компонент для страниц с кандидатами

import { ref } from 'vue';
import router from '@router/router';
import NavBar from '@layouts/NavBar.vue'
import AlertMessage from '@layouts/AlertMessage.vue';

// Аттрибут и текст сообщения на странице
const data = ref({
  attr: '',
  text: ''
})

router.push({ name: 'persons' }) // Переход на страницу с кандидатами

// Обновление сообщения
function updateMessage(alert: Object){
  data.value.attr = (alert as { attr: string })["attr"];
  data.value.text = (alert as { text: string })["text"];
}

</script>

<template>
    <NavBar />
    <AlertMessage v-if="data.attr" :attr="data.attr" :text="data.text" />
    <router-view @updateMessage="updateMessage" />
</template>