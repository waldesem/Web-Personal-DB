<script setup lang="ts">

import { alertStore } from '@store/alert';

const storeAlert = alertStore();

</script>

<template>
  <div class="container py-3">
    <div class="alert" :class="storeAlert.alertMessage.attrAlert" role="info" fade show>
      {{storeAlert.alertMessage.textAlert}}
    </div>
  </div>
</template>