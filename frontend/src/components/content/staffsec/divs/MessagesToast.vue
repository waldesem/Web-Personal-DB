<script setup lang="ts">
import { timeSince } from "@utilities/utils";
import { Message } from "@/interfaces/interface";

const props = defineProps({
  messages: {
    type: Array as () => Array<Message>,
    default: () => [{}]
  },
});
</script>

<template>
  <div
    v-if="props.messages.length"
    class="toast-container position-static"
  >
    <div
      class="toast"
      role="alert"
      aria-live="assertive"
      aria-atomic="true"
      v-for="(message, index) in props.messages"
      :key="index"
    >
      <div class="toast-header">
        <small class="text-body-secondary">
          {{ timeSince(message["created"]) }}
        </small>
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="toast"
          aria-label="Close"
        ></button>
      </div>
      <div class="toast-body">
        {{ message["message"] }}
      </div>
    </div>
  </div>
</template>
