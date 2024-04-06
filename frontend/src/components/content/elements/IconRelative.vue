<script setup lang="ts">
const emit = defineEmits(["onclick"]);
const props = defineProps({
  title: String,
  iconClass: String,
  disable: {
    type: Boolean,
    default: false,
  }
})
</script>

<template>
  <div class="position-relative flex-grow-1">
    <a
      role="button"
      class="d-print-none"
      @click="emit('onclick')"
      :disabled="props.disable"
    >
      <i
        :class="props.iconClass"
        :title="props.title"
        style="cursor: pointer"
      >
      </i>
      <slot></slot>
    </a>
  </div>
</template>