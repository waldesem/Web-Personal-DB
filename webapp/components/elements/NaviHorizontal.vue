<script setup lang="ts">
const emit = defineEmits(["delete", "update", "upload"]);

const links = [{
  label: 'Изменить',
  icon: 'i-heroicons-pencil-square',
  click: () => emit('update')
}, {
  label: 'Удалить',
  icon: 'i-heroicons-trash',
  click: () => emit('delete')
}, {
  label: 'Загрузить',
  icon: 'i-heroicons-cloud-arrow-up',
  slot: 'upload',
  click: () => emit('upload')
}]
</script>

<template>
  <UHorizontalNavigation :links="links" class="border-t "/>
</template>