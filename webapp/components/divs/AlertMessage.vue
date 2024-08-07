<script setup lang="ts">
import { stateAlert } from "@/state/state";
const alertState = stateAlert();
</script>

<template>
  <div
    v-show="alertState.alertMessage.value.show"
    class="alert"
    role="alert"
    fade
    show
    :class="alertState.alertMessage.value.attr"
  >
    {{ alertState.alertMessage.value.text }}
  </div>
</template>
