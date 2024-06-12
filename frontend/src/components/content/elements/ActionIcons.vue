<script setup lang="ts">
const emit = defineEmits(["delete", "update"]);
const props = defineProps({
  hide: {
    type: Boolean,
    default: false
  },
  disable: {
    type: Boolean,
    default: false
  },
  showForm: {
    type: Boolean,
    default: false
  }
})
</script>

<template>
  <div class="position-relative d-print-none">
    <div class="position-absolute top-0 end-0">
      <a
        :hidden="props.hide"
        class="btn btn-link"
        title="Изменить"
        @click="emit('update')"
      >
        <i class="bi bi-pencil-square"></i>
      </a>
      <a 
        class="btn btn-link"
        title="Удалить"
        :disabled="props.disable"
        @click="emit('delete')" 
      >
        <i class="bi bi-trash"></i>
      </a>
      <label v-if="props.showForm" for="file">
        <a class="btn btn-link" title="Загрузить">
        <i class="bi bi-cloud-arrow-up-fill"></i>
        </a>
      </label>  
      <slot></slot>
    </div>
  </div>
</template>