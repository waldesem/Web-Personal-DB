<script setup lang="ts">
const emit = defineEmits(["delete", "update"]);
const props = defineProps({
  hide: {
    type: Boolean,
    default: false,
  },
  forInput: {
    type: String,
    default: "file",
  },
});
</script>

<template>
  <div class="position-relative d-print-none">
    <div class="position-absolute top-0 end-0">
      <button class="btn btn-link" title="Изменить" @click="emit('update')">
        <div class="fs-6 text-primary"><i class="bi bi-pencil-square"></i></div>
      </button>
      <button class="btn btn-link" title="Удалить" @click="emit('delete')">
        <div class="fs-6 text-danger"><i class="bi bi-trash"></i></div>
      </button>
      <label
        class="text-body-secondary fs-5 mt-2"
        :for="props.forInput"
        :hidden="props.hide"
        style="cursor: pointer"
      >
        <i class="bi bi-cloud-arrow-up"></i>
      </label>
      <slot></slot>
    </div>
  </div>
</template>

<style scoped>
.btn {
  text-decoration: none;
}
</style>
