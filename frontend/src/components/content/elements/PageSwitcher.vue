<script setup lang="ts">
const props = defineProps({
  has_prev: Boolean,
  has_next: Boolean,
  switchPrev: Number,
  switchNext: Number,
});

const emit = defineEmits(["switch"])
</script>

<template>
  <nav 
    class="d-flex justify-content-center mb-3"
    v-if="props.has_prev || props.has_next">
    <ul class="pagination justify-content-center">
      <li v-bind:class="{ 'page-item': true, disabled: !props.has_prev }">
        <a
          class="page-link"
          href="#"
          @click="$emit('switch', props.switchPrev)"
        >
          Предыдущая
        </a>
      </li>
      <li v-bind:class="{ 'page-item': true, disabled: !props.has_next }">
        <a
          class="page-link"
          href="#"
          @click="$emit('switch', props.switchNext)"
        >
          Следующая
        </a>
      </li>
    </ul>
  </nav>
</template>
