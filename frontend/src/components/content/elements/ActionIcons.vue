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
        <div class="fs-5">&plusmn;</div>
      </a>
      <a 
        class="btn btn-link"
        title="Удалить"
        @click="emit('delete')" 
      >
        <div class="fs-5">&times;</div>
      </a>
      <label 
        :for="props.forInput"
        :hidden="props.hide"
      >
        <a class="btn btn-link" title="Загрузить">
          <div class="fs-5">&infin;</div>
        </a>
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