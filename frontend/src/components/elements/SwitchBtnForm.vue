<script setup lang="ts">
const props = defineProps({
  subj: String,
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
    @click="props.switchForm(props.subj)"
    :title="props.flag === props.subj ? 'Закрыть форму' : 'Добавить информацию'"
  >
    <i
      :class="
        props.flag === props.subj ? 'bi bi-dash-circle' : 'bi bi-plus-circle'
      "
    ></i>
  </a>
</template>
