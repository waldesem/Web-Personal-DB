<script setup lang="ts">
cost props = defineProps({
  edit: {
    type: Boolean, 
    default: false 
    }, 
  candId: {
    type: String, 
    default: ""
    },
  person: {
    type: Object as Persons, 
    default: {} as Persons{}
  }
}

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
    <template #resume=""><DivsResumeDiv :candId: "props.candId" :edit"props.edit" :person="props.person" /></template>
    <template #staff=""><DivsStaffDiv :candId: "props.candId" :edit"props.edit"/></template>
    <template #education=""><DivsEducateDiv :candId: "props.candId" :edit"props.edit"/></template>
    <template #work=""><DivsWorkDiv :candId: "props.candId" :edit"props.edit"/></template>
    <template #document=""><DivsDocumDiv :candId: "props.candId" :edit"props.edit" /></template>
    <template #address=""><DivsAddressDiv /></template>
    <template #contact=""><DivsContactDiv :candId: "props.candId" :edit"props.edit" /></template>
    <template #affiliation=""><DivsAffilDiv :candId: "props.candId" :edit"props.edit" /></template>
    <template #prev=""><DivsPrevDiv :candId: "props.candId" :edit"props.edit" /></template>
    <template #relate=""><DivsRelateDiv :candId: "props.candId" :edit"props.edit" /></template>
  </UAccordion>
</template>
