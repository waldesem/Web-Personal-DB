<script setup lang="ts">
const props = defineProps({
  modal: {
    type: Boolean,
    default: false,
  },
});
</script>

<template>
  <UModal
    v-model:open="props.modal"
    :overlay="true"
    :dismissible="false"
    :ui="{
      content:
        'fixed bg-default divide-y divide-default flex flex-col focus:outline-none',
      header: 'flex items-center gap-1.5 p-4 sm:px-6 min-h-16',
    }"
  >
    <UProgress animation="swing" />
  </UModal>
</template>
