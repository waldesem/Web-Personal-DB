<script setup lang="ts">
const props = defineProps({
  elemId: String
})
</script>

<template>
    <div class="modal modal fade" :id="props.elemId" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-body">
          <slot></slot>
        </div>
      </div>
    </div>
  </div>
</template>