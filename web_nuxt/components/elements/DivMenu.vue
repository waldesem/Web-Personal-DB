<script setup lang="ts">
const emit = defineEmits(["delete", "update", "create"]);

const props = defineProps({
  items: {
    type: Number,
    default: 0,
  },
});

const options = [
  {
    label: "Добавить",
    icon: "i-heroicons-document-plus",
    disabled: false,
    click: () => emit("create"),
  },
  {
    label: "Изменить",
    icon: "i-heroicons-pencil-square",
    disabled: !props.items,
    click: () => emit("update"),
  },
  {
    label: "Удалить",
    icon: "i-heroicons-trash",
    disabled: !props.items,
    click: () => emit("delete"),
  },
];
</script>

<template>
  <UButton
    v-for="(option, idx) in options"
    :key="idx"
    :disabled="option.disabled"
    :icon="option.icon"
    :label="option.label"
    variant="ghost"
    @click="option.click"
  />
</template>
