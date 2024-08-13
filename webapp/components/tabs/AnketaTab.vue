<script setup lang="ts">
const items = [
  {
    label: "Резюме",
    icon: "i-heroicons-user",
    defaultOpen: true,
    slot: "resume",
  },
  {
    label: "Должности",
    icon: "i-heroicons-briefcase",
    slot: "staff",
  },
  {
    label: "Образование",
    icon: "i-heroicons-academic-cap",
    slot: "education",
  },
  {
    label: "Работа",
    icon: "i-heroicons-briefcase",
    slot: "work",
  },
  {
    label: "Документы",
    icon: "i-heroicons-document-text",
    slot: "document",
  },
  {
    label: "Адреса",
    icon: "i-heroicons-home-modern",
    slot: "address",
  },
  {
    label: "Контакты",
    icon: "i-heroicons-phone",
    slot: "contact",
  },
  {
    label: "Аффилированные",
    icon: "i-heroicons-user-group",
    slot: "affiliation",
  },
  {
    label: "Изменения имени",
    icon: "i-heroicons-archive-box-arrow-down",
    slot: "prev",
  },
  {
    label: "Связанные",
    icon: "i-heroicons-user-group",
    slot: "relate",
  },
];
</script>

<template>
  <UAccordion :items="items" size="lg" multiple>
    <template #resume=""><DivsResumeDiv /></template>
    <template #staff=""><DivsStaffDiv /></template>
    <template #education=""><DivsEducateDiv /></template>
    <template #work=""><DivsWorkDiv /></template>
    <template #document=""><DivsDocumDiv /></template>
    <template #address=""><DivsAddressDiv /></template>
    <template #contact=""><DivsContactDiv /></template>
    <template #affiliation=""><DivsAffilDiv /></template>
    <template #prev=""><DivsPrevDiv /></template>
    <template #relate=""><DivsRelateDiv /></template>
  </UAccordion>
</template>
