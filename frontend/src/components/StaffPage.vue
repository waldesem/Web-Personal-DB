<script setup lang="ts">

import { ref } from 'vue';
import NavBar from './NavBar.vue'
import router from '../router/router';
import AlertMessage from './AlertMessage.vue';

const data = ref({
  attr: '',
  text: ''
})

router.push({ name: 'persons' })

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