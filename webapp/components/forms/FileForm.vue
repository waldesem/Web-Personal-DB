<script setup lang="ts">
const props = defineProps({
  label: {
    type: String,
    default: "Файл",
  },
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
    <UFormGroup class="mb-3" size="md" label="Файл">
      <UInput
        v-show="props.display"
        :id="props.nameId"
        type="file"
        :accept="props.accept"
        multiple
      />
    </UFormGroup>
  </UForm>
</template> 
