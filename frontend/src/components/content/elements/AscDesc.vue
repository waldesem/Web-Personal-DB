<script setup lang="ts">
const emit = defineEmits(["get-candidates"]);
const props = defineProps({
  sort: {
    type: String,
    default: "id",
  },
  order: {
    type: String,
    default: "desc",
  }
})

</script>

<template>
  <a 
    role="button" 
    @click="
      emit('get-candidates', props.sort, props.order)
    "
  >
    <i 
      :title="props.order === 'desc' ? 'Сортировка по убыванию' : 'Сортировка по возрастанию'"
      class="bi"
      :class="props.order === 'desc' 
        ? 'bi-caret-down-fill' 
        : 'bi-caret-up-fill'"
    >
    </i>
  </a>
</template>

<style scoped>
.a {
  padding: 0;
  margin: 0;
}
</style>