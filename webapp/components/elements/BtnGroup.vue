<script setup lang="ts">
const emit = defineEmits(["cancel"]);
</script>

<template>
  <UButtonGroup class="mt-3" size="md" orientation="horizontal">
    <UButton
      label="Принять"
      color="green"
      variant="outline"
      type="submit"
    />
    <UButton
      label="Отмена"
      color="red"
      variant="outline"
      @click="emit('cancel')"
    />
  </UButtonGroup>
</template>