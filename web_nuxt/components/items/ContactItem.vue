<script setup lang="ts">

const props = defineProps({
  item: {
    type: Object as PropType<Contact>,
    default: () => ({}),
  },
});

const contact = {
  Вид: props.item.view,
  Контакт: props.item.contact,
};
</script>

<template>
  <div v-for="(value, key) in contact" :key="key">
    <ElementsLabelValue :label="key" :value="value" />
  </div>
</template>
