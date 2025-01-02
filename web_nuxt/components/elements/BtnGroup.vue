<script setup lang="ts">
const emit = defineEmits(["cancel"]);
</script>

<template>
  <div class="mt-3">
    <UButtonGroup>
      <UButton label="Принять" color="green" variant="outline" type="submit" />
      <UButton label="Очистить" color="blue" variant="outline" type="reset" />
      <UButton
        label="Отмена"
        color="red"
        variant="outline"
        @click="emit('cancel')"
      />
    </UButtonGroup>
  </div>
</template>
