<script setup lang="ts">
const props = defineProps({
  id: String,
  header: String,
});
</script>

<template>
  <h6>
    <button
      type="button"
      class="btn btn-link"
      data-bs-toggle="collapse"
      :href="`#${props.id}`"
    >
    {{ props.header }}
    </button>
  </h6>
</template>
