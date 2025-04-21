<script setup lang="ts">
await preloadComponents([
  "DivsResumeDiv",
  "DivsPrevDiv",
  "DivsStaffDiv",
  "DivsEducateDiv",
  "DivsWorkDiv",
  "DivsDocumDiv",
  "DivsAddressDiv",
  "DivsContactDiv",
  "DivsRelateDiv",
  "DivsAffilDiv",
]);

const emit = defineEmits(["update"]);
</script>

<template>
  <DivsResumeDiv @update="emit('update')" />
  <DivsStaffDiv />
  <DivsEducateDiv />
  <DivsWorkDiv />
  <DivsDocumDiv />
  <DivsAddressDiv />
  <DivsContactDiv />
  <DivsPrevDiv />
  <DivsRelateDiv />
  <DivsAffilDiv />
</template>
