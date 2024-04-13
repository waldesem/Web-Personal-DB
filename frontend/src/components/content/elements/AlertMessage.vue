<script setup lang="ts">
import { alertStore } from "@store/alert";

const storeAlert = alertStore();
</script>

<template>
  <div
    class="alert"
    role="info"
    fade
    show
    :class="storeAlert.alertMessage.attr"
  >
    {{ storeAlert.alertMessage.text }}
  </div>
</template>
