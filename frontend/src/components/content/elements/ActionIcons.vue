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
      <button
        class="btn btn-link"
        title="Изменить"
        @click="emit('update')"
      >
        <div class="fs-5 text-primary">&plusmn;</div>
      </button>
      <button 
        class="btn btn-link"
        title="Удалить"
        @click="emit('delete')" 
      >
        <div class="fs-5 text-danger">&times;</div>
      </button>
      <label 
        :for="props.forInput"
        :hidden="props.hide"
      >
        <button class="btn btn-link" title="Загрузить">
          <div class="fs-5 text-secondary">&infin;</div>
        </button>
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