<script setup lang="ts">
const props = defineProps({
  accept: String,
  nameId: {
    type: String,
    default: "file",
  },
  display: {
    type: Boolean,
    default: false,
  }
});
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
      v-show="props.display"
      class="form-control form-control-sm"
      :class="props.display ? 'visible' : 'hidden'"
      :id="props.nameId"
      :name="props.nameId"
      type="file"
      :accept="props.accept"
      ref="file"
      multiple
    />
  </form>
</template> 
