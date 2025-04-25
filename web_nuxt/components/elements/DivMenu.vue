<script setup lang="ts">
const emit = defineEmits(["delete", "update"]);
</script>

<template>
  <UButton
    icon="i-heroicons-pencil-square"
    label="Изменить"
    variant="ghost"
    @click="emit('update')"
  />
  <UButton
    icon="i-heroicons-trash"
    label="Удалить"
    variant="ghost"
    @click="emit('delete')"
  />
</template>
