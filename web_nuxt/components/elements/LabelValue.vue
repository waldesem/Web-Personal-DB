<script setup lang="ts">
// Компонент для отображения лейбла и значения в виде строки или объекта(компонента)
const props = defineProps({
  label: {
    type: String,
    default: "",
  },
  value: {
    type: [String, Number, Object],
    default: "",
  },
});
</script>

<template>
  <div v-if="props.value" class="flex grid grid-cols-12 gap-3 mb-4">
    <div class="col-span-3">{{ props.label }}</div>
    <div v-if="typeof props.value === 'object'" class="col-span-9">
      <component :is="props.value" />
    </div>
    <div v-else class="col-span-9 break-words">{{ props.value }}</div>
  </div>
</template>
