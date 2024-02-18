<script setup lang="ts">
const props = defineProps({
  item: String,
  flag: String,
  switchForm: {
    type: Function,
    required: true,
  },
});
</script>

<template>
  <a
    class="btn btn-link"
    @click="props.switchForm(props.item)"
    :title="props.flag === props.item ? 'Закрыть форму' : 'Добавить информацию'"
  >
    <i
      :class="
        props.flag === props.item ? 'bi bi-dash-circle' : 'bi bi-plus-circle'
      "
    ></i>
  </a>
</template>
