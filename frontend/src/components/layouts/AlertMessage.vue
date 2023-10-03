<script setup lang="ts">
// Компонент для отображения сообщений

import { alertStore } from '@store/alert';

const storeAlert = alertStore();

</script>

<template>
  <div class="container py-3">
    <div class="alert" :class="storeAlert.alertAttr" role="info" fade show>
      {{storeAlert.alertText}}
    </div>
  </div>
</template>