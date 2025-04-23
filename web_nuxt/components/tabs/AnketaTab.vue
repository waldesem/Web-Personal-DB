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
  <div
    v-for="(items, idx) in [
      [DivsStaffDiv, 'Должности'],
      [DivsEducateDiv, 'Образование'],
      [DivsWorkDiv, 'Место работы'],
      [DivsDocumDiv, 'Документы'],
      [DivsAddressDiv, 'Адреса'],
      [DivsContactDiv, 'Контакты'],
      [DivsPrevDiv, 'Изменения имени'],
      [DivsRelateDiv, 'Связанные лица'],
      [DivsAffilDiv, 'Аффилированность'],
    ]"
    :key="idx"
  >
    <UCollapsible class="m-2">
      <UButton
        :label="items[1]"
        icon="i-heroicons-home-modern"
        color="neutral"
        variant="subtle"
        trailing-icon="i-lucide-chevron-down"
        block
      />
      <template #content><component :is="items[0]" /></template>
    </UCollapsible>
  </div>
</template>
