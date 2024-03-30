<script setup lang="ts">
const emit = defineEmits(["submit"]);
</script>

<template>
  <form
    @submit.prevent="$emit('submit', $event)"
    class="form form-check"
    role="form"
  >
    <slot></slot>
  </form>
</template>