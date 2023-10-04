<script setup lang="ts">
// Компонент для отображения сообщений

import { alertStore } from '@store/alert';

const storeAlert = alertStore();

</script>

<template>
  <div class="container py-3">
    <div class="alert" :class="storeAlert.attrAlert" role="info" fade show>
      {{storeAlert.textAlert}}
    </div>
  </div>
</template>