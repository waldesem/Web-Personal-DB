<script setup lang="ts">
const emit = defineEmits(["onclick"]);
const props = defineProps({
  title: String,
  iconClass: String,
  hide: {
    type: Boolean,
    default: false,
  }
})
</script>

<template>
  <div class="position-relative flex-grow-1">
    <button
      type="button"
      class="btn btn-link"
      @click="emit('onclick')"
      :disabled="props.hide"
    >
      <i
        :class="props.iconClass"
        :title="props.title"
        style="cursor: pointer"
      >
      </i>
      <slot></slot>
    </button>
  </div>
</template>