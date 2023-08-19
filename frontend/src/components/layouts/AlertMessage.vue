<script setup lang="ts">
// Компонент для отображения сообщений

import { appAlert } from '@store/alert';

const alertStore = appAlert();

</script>

<template>
  <div class="container py-3">
    <div class="alert" :class="alertStore.alertAttr" role="info" fade show>{{alertStore.alertText}}</div>
  </div>
</template>