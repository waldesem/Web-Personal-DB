<script setup lang="ts">
import { ref } from 'vue';

const emit = defineEmits(["action"]);
const props = defineProps({
  id: String,
  header: String,
  action: String,
  printPage: {
    type: Boolean,
    default: false,
  },
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
      v-if="!props.printPage"
      :disabled="props.disable"
      type="button"
      class="btn btn-link"
      title="Добавить информацию"
      @click="emit('action')"
    >
      <i 
        :class="props.action ? 'bi bi-database-slash' : 'bi-database-up'"
      ></i>
    </button>
    <button
      type="button"
      class="btn btn-link"
      data-bs-toggle="collapse"
      :href="`#${props.id}`"
      :title="toggle ? 'Развернуть' : 'Свернуть'"
      @click="toggle = !toggle"
    >
      {{ props.header }}
   </button>
  </h6>
</template>