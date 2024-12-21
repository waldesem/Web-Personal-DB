<script setup lang="ts">

const emit = defineEmits(["delete", "update"]);

defineProps({
  isChanged: {
    type: Boolean,
    default: true,
  },
});

const links = [
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
  <UHorizontalNavigation :links="isChanged ? links : links.slice(0, 1)" />
</template>
