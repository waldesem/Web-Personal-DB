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
    <div class="btn-group">
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
      <button
        type="button"
        class="btn btn-link dropdown-toggle dropdown-toggle-split d-print-none"
        data-bs-toggle="dropdown"
        title="Добавить информацию"
      >
      </button>
      <ul class="dropdown-menu">
        <li>
          <a 
            class="dropdown-item btn btn-link" 
            role="button"
            @click="emit('action')">Добавить</a>
        </li>
      </ul>
    </div>
  </h6>
</template>