<script setup lang="ts">
const emit = defineEmits(["delete", "update", "create"]);

const props = defineProps({
  items: {
    type: Number,
    default: 0,
  },
})

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
  <UButton
    label="Добавить"
    variant="ghost"
    icon="i-heroicons-document-plus"
    @click="emit('create')"
  />
  <UButton
    v-for="option in options"
    :key="option.label"
    :disabled="props.items == 0"
    :icon="option.icon"
    :label="option.label"
    variant="ghost"
    @click="option.click"
  />
</template>
