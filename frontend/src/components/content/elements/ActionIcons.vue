<script setup lang="ts">
const emit = defineEmits(["delete", "update"]);
const props = defineProps({
  hide: {
    type: Boolean,
    default: false
  }
})
</script>

<template>
  <a 
    class="btn btn-link"
    title="Удалить"
    @click="emit('delete')" 
  >
    <i class="bi bi-trash"></i>
  </a>
  <a
    :hidden="props.hide"
    class="btn btn-link"
    title="Изменить"
    @click="emit('update')"
  >
    <i class="bi bi-pencil-square"></i>
  </a>
</template>