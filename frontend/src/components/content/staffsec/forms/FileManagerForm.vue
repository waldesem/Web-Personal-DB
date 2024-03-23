<script setup lang="ts">
const model = defineModel();
const emit = defineEmits(["update-item"]);
</script>

<template>
  <form
    @submit.prevent="emit('update-item')"
    class="form form-check"
    role="form"
    >
    <div class="row">
      <div class="col">
      <input
        class="form-control"
        id="name"
        maxlength="250"
        name="name"
        type="text"
        v-model="model"
      />
      </div>
      <div class="col">
      <button
        class="btn btn-primary btn-md"
        data-bs-dismiss="modal"
        name="submit"
        type="submit"
      >
        Принять
      </button>
      </div>
    </div>
  </form>
</template>