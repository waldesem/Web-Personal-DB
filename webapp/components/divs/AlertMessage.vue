<script setup lang="ts">
import { stateAlert } from "@/utils/state";
</script>

<template>
  <div
    v-show="stateAlert.alertMessage.show"
    class="alert"
    role="alert"
    fade
    show
    :class="stateAlert.alertMessage.attr"
  >
    {{ stateAlert.alertMessage.text }}
  </div>
</template>
