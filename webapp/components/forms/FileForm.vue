<script setup lang="ts">
const props = defineProps({
  accept: {
    type: String,
    default: "*",
  },
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
  <UForm 
    enctype="multipart/form-data"
    @change="emit('submit', $event)" 
    >
    <UInput
      v-show="props.display"
      :id="props.nameId"
      type="file"
      :accept="props.accept"
      multiple
    />
  </UForm>
</template> 
