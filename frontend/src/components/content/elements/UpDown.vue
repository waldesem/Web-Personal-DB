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
    class="btn btn-link" @click="
      emit('get-candidates', props.sort, props.order)
    "
  >
    <i 
      class="bi"
      :class="props.order === 'desc' 
        ? 'bi-caret-down-fill' 
        : 'bi-caret-up-fill'"
    >
    </i>
  </a>
</template>