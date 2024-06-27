<script setup lang="ts">
const props = defineProps({
  title: String,
  id: String,
  iconClass: String,
  hide: {
    type: Boolean,
    default: false,
  }
})
</script>

<template>
  <div class="position-relative text-end flex-grow-1">
    <button
      type="button"
      class="btn btn-link"
      :disabled="props.hide"
      data-bs-toggle="collapse"
      :href="`#${props.id}`"
    >
      <i
        :class="props.iconClass"
        :title="props.title"
        style="cursor: pointer"
      >
      </i>
    </button>
  </div>
</template>