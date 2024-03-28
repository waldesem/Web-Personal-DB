<script setup lang="ts">
import { ref } from "vue";

const props = defineProps({
  id: String,
  idx: {
    type: String,
    required: true,
  },
  label: String,
});

const toggle = ref(true);
</script>

<template>
  <div class="mb-3 ms-3">
    <a
      class="link-primary"
      role="button"
      data-bs-toggle="collapse"
      :href="`#${props.id}`"
      @click="toggle = !toggle"
    >
      {{ props.label }}
    </a>
    <div class="collapse show" :id="props.id">
      <slot></slot>
    </div>
  </div>
</template>
