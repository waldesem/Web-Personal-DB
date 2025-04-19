<script setup lang="ts">

const emit = defineEmits(["delete", "update"]);

const items = [
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
  <UNavigationMenu variant="link" :items="items" />
</template>
