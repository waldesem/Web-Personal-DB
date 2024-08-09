<script setup lang="ts">
import { stateAlert } from "@/state/state";
const alertState = stateAlert();
</script>

<template>
  <UAlert
    v-show="alertState.alertMessage.value.show"
    :color="alertState.alertMessage.value.attr"
    :title="alertState.alertMessage.value.title"
    :description="alertState.alertMessage.value.text"
    />
</template>
