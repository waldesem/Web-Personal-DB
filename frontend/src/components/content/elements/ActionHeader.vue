<script setup lang="ts">
import { ref } from 'vue';

const emit = defineEmits(["action"]);
const props = defineProps({
  id: String,
  header: String,
  action: String,
});
const toggle = ref(true); 
</script>

<template>
  <h6>
    <a
      class="link-primary"
      role="button"
      data-bs-toggle="collapse"
      :href="`#${props.id}`"
      :title="toggle ? 'Развернуть' : 'Свернуть'"
      @click="toggle = !toggle"
    >
      {{ props.header }}
    </a>
    <a
      class="btn btn-link"
      title="Добавить информацию"
      @click="emit('action')"
    >
      <i
        :class="props.action ? 'bi bi-plus-square-dotted' : 'bi bi-plus-square'"
      ></i>
    </a>
  </h6>
</template>