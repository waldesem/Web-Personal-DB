<script setup lang="ts">

const emit = defineEmits(["delete", "update"]);

const options = [
  {
    label: "Удалить",
    icon: "i-heroicons-trash",
    click: () => emit("delete"),
  },
  {
    label: "Изменить",
    icon: "i-heroicons-pencil-square",
    click: () => emit("update"),
  },
];
</script>

<template>
  <UButtonGroup>
    <UButton
      v-for="option in options"
      :key="option.label"
      :icon="option.icon"
      :label="option.label"
      variant="ghost"
      @click="option.click"
    />
  </UButtonGroup>
</template>
