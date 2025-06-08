<script setup lang="ts">

const props = defineProps({
  item: {
    type: Object as PropType<Staff>,
    default: () => ({}),
  },
});

const staff = {
  Должность: props.item.position,
  Департамент: props.item.department,
};
</script>

<template>
  <div v-for="(value, key) in staff" :key="key">
    <ElementsLabelValue :label="key" :value="value" />
  </div>
</template>
