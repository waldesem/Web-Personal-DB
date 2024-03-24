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
      <div class="col input-group">
        <input
          class="form-control"
          id="name"
          maxlength="250"
          name="name"
          type="text"
          v-model="model"
        />
        <span class="input-group-text">
          <a
            role="button"
            name="submit"
            type="submit"
          >
            <i class="bi bi-save"></i>
        </a>
        </span>
      </div>
    </div>
  </form>
</template>