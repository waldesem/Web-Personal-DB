<script setup lang="ts">
const prop = defineProps(["accept"]);
const emit = defineEmits(["submit"])
</script>

<template>
  <form 
    class="form form-check" 
    role="form" 
    @change="emit('submit', $event)" 
    enctype="multipart/form-data"
  >
    <input
      class="form-control form-control-sm invisible"
      id="file"
      name="file"
      type="file"
      :accept="prop.accept"
      ref="file"
      multiple
    />
  </form>
</template>

<style scoped>
input[type="file"] {
  display: none;
}
</style>