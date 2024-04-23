<script setup lang="ts">
const emit = defineEmits(["sort-candidates"]);
const props = defineProps({
  sort: {
    type: String,
    default: "id",
  },
  order: {
    type: String,
    default: "desc",
  },
});
</script>

<template>
  <i
    @click="emit('sort-candidates', props.sort, props.order)"
    :title="
      props.order === 'desc'
        ? 'Сортировка по убыванию'
        : 'Сортировка по возрастанию'
    "
    class="bi"
    :class="
      props.order === 'desc' ? 'bi-caret-down-fill' : 'bi-caret-up-fill'
    "
  >
  </i>
</template>

<style scoped>
.a {
  padding: 0;
  margin: 0;
}
</style>
