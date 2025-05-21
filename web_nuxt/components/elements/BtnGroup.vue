<script setup lang="ts">
const emit = defineEmits(["cancel"]);
</script>

<template>
  <div class="mt-3">
    <UButtonGroup>
      <UButton
        label="Принять"
        color="success"
        variant="outline"
        type="submit"
      />
      <UButton
        label="Очистить"
        color="secondary"
        variant="outline"
        type="reset"
      />
      <UButton
        label="Отмена"
        color="error"
        variant="outline"
        @click="emit('cancel')"
      />
    </UButtonGroup>
  </div>
</template>
