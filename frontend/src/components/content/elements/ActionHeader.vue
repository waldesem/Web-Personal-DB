<script setup lang="ts">
import { ref } from 'vue';

const emit = defineEmits(["action"]);
const props = defineProps({
  id: String,
  header: String,
  action: String,
  disable: {
    type: Boolean,
    default: false,
  }
});
const toggle = ref(true); 
</script>

<template>
  <h6>
    <button
      type="button"
      class="link link-primary"
      data-bs-toggle="collapse"
      :href="`#${props.id}`"
      :title="toggle ? 'Развернуть' : 'Свернуть'"
      @click="toggle = !toggle"
    >
      {{ props.header }}
   </button>
    <button
      :disabled="!props.disable"
      type="button"
      class="link link-primary"
      title="Добавить информацию"
      @click="emit('action')"
    >
      <i
        :class="props.action ? 'bi bi-plus-square-dotted' : 'bi bi-plus-square'"
      ></i>
    </button>
  </h6>
</template>