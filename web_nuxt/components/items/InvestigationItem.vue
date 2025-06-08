<script setup lang="ts">

const props = defineProps({
  item: {
    type: Object as PropType<Inquisition>,
    default: () => ({}),
  },
});

const investigation = {
  "Тема проверки": props.item.theme,
  Информация: props.item.info,
  "Дата записи": props.item.created
    ? new Date(props.item.created).toLocaleString("ru-RU").split(",")[0]
    : "",
};
</script>

<template>
  <div v-for="(value, key) in investigation" :key="key">
    <ElementsLabelValue :label="key" :value="value" />
  </div>
</template>
