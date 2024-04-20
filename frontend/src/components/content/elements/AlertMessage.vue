<script setup lang="ts">
import { stateAlert } from "@/state";
</script>

<template>
  <div
    class="alert"
    role="info"
    fade
    show
    :class="stateAlert.alertMessage.attr"
  >
    {{ stateAlert.alertMessage.text }}
  </div>
</template>
