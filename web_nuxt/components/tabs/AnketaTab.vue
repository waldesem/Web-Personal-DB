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

const items = [
  {
    label: "Резюме",
    icon: "i-heroicons-user",
    slot: "resume" as const,
  },
  {
    label: "Должности",
    icon: "i-heroicons-briefcase",
    slot: "staff" as const,
  },
  {
    label: "Образование",
    icon: "i-heroicons-academic-cap",
    slot: "education",
  },
  {
    label: "Работа",
    icon: "i-heroicons-briefcase",
    slot: "work" as const,
  },
  {
    label: "Документы",
    icon: "i-heroicons-document-text",
    slot: "document" as const,
  },
  {
    label: "Адреса",
    icon: "i-heroicons-home-modern",
    slot: "address" as const,
  },
  {
    label: "Контакты",
    icon: "i-heroicons-phone",
    slot: "contact" as const,
  },
  {
    label: "Аффилированные",
    icon: "i-heroicons-user-group",
    slot: "affiliation" as const,
  },
  {
    label: "Изменения имени",
    icon: "i-heroicons-archive-box-arrow-down",
    slot: "prev" as const,
  },
  {
    label: "Связанные",
    icon: "i-heroicons-user-group",
    slot: "relate" as const,
  },
];
</script>

<template>
  <UAccordion :items="items" type="multiple" default-value="resume">
    <template #resume="">
      <DivsResumeDiv @update="emit('update')" />
    </template>
    <template #prev="">
      <DivsPrevDiv />
    </template>
    <template #staff="">
      <DivsStaffDiv />
    </template>
    <template #education="">
      <DivsEducateDiv />
    </template>
    <template #work="">
      <DivsWorkDiv />
    </template>
    <template #document="">
      <DivsDocumDiv />
    </template>
    <template #address="">
      <DivsAddressDiv />
    </template>
    <template #contact="">
      <DivsContactDiv />
    </template>
    <template #affiliation="">
      <DivsAffilDiv />
    </template>
    <template #relate="">
      <DivsRelateDiv />
    </template>
  </UAccordion>
</template>
