<script setup lang="ts">
const prop = defineProps(["accept"]);
const emit = defineEmits(["submit"])
</script>

<template>
  <form
    class="form form-check"
    enctype="multipart/form-data"
    role="form"
    @change="emit('submit', $event)"
  >
    <input
      class="form-control"
      id="file"
      type="file"
      :accept="prop.accept"
      ref="file"
    />
  </form>
</template>

<style scoped>
.form {
  display: flex;
}
</style>