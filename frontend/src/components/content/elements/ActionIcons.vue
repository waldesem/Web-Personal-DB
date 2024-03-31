<script setup lang="ts">
const emit = defineEmits(["delete", "update"]);
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
    class="btn btn-link"
    title="Изменить"
    @click="emit('update')"
  >
    <i class="bi bi-pencil-square"></i>
  </a>
</template>