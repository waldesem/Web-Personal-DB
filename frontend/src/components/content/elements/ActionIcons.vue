<script setup lang="ts">
const emit = defineEmits(["delete", "update"]);
const props = defineProps({
  hide: {
    type: Boolean,
    default: false,
  },
  forInput: {
    type: String,
    default: "file"
  }
})
</script>

<template>
  <div class="position-relative d-print-none">
    <div class="position-absolute top-0 end-0">
      <a
        class="btn btn-link"
        title="Изменить"
        @click="emit('update')"
      >
        <i class="bi bi-pencil-square"></i>
      </a>
      <a 
        class="btn btn-link"
        title="Удалить"
        @click="emit('delete')" 
      >
        <i class="bi bi-trash"></i>
      </a>
      <label 
        :for="props.forInput"
        :hidden="props.hide"
      >
        <a class="btn btn-link" title="Загрузить">
          <i class="bi bi-cloud-arrow-up-fill"></i>
        </a>
      </label>  
      <slot></slot>
    </div>
  </div>
</template>