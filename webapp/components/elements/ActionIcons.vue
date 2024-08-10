<script setup lang="ts">
const emit = defineEmits(["delete", "update"]);
</script>

<template>
  <div class="relative">
    <div class="absolute object-right">
      <UButton
        title="Изменить" 
        icon="i-heroicons-pencil-square"
        @click="emit('update')"/>
      <UButton
        title="Удалить"
        icon="i-heroicons-trash"
        @click="emit('delete')"/>
      <slot/>
    </div>
  </div>
</template>
