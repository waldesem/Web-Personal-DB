<script setup lang="ts">
const props = defineProps({
  id: String,
  title: String,
  size: {
    type: String,
    default: "modal-xl",
  },
});
</script>

<template>
  <div 
    class="modal fade" 
    data-bs-backdrop="static"
    data-bs-keyboard="false"
    :id="props.id" 
    tabindex="-1"
  >
    <div
      class="modal-dialog modal-dialog-centered"
      :class="props.size"
      data-bs-keyboard="false"
      role="document"
    >
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5">
            {{ props.title }}
          </h1>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <slot></slot>
        </div>
      </div>
    </div>
  </div>
</template>
