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
    href="#" 
    @click="emit('delete')" 
    title="Удалить"
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