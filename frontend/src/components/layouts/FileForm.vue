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
    <div class="mb-3 row">
      <label class="col-form-label col-lg-2" for="file">Загрузить файл</label>
      <div class="col-lg-10">
        <input
          class="form-control"
          id="file"
          type="file"
          :accept="prop.accept"
          ref="file"
        />
      </div>
    </div>
  </form>
</template>
