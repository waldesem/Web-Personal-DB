<script setup lang="ts">
const emit = defineEmits(["action"]);
const props = defineProps({
  header: String,
  action: String,
});
</script>

<template>
  <h6>
    {{ props.header }}
    <a
      class="btn btn-link"
      title="Добавить информацию"
      @click="emit('action')"
    >
    <i
        :class="props.action ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"
      ></i>
    </a>
  </h6>
</template>