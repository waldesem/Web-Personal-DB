<script setup lang="ts">
// Компонент для отображения сообщений

const props = defineProps({
  attr: String,
  text: String
});

</script>

<template>
  <div class="container py-3">
    <div class="alert" :class="props.attr" role="info" fade show>{{props.text}}</div>
  </div>
</template>