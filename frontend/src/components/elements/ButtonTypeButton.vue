<script setup lang="ts">

const props = defineProps({
  class: String,
  name: String,
  func: Function
})

</script>

<template>
  <button @click="props.func" type="button" :class="`btn btn-outline-${props.class}`">
    {{ props.name }}
  </button>
</template>