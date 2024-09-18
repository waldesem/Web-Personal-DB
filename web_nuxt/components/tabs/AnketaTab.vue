<script setup lang="ts">
import type { Persons } from "@/types/interfaces";

const props = defineProps({
  editable: {
    type: Boolean,
    default: false,
  },
  candId: {
    type: String,
    default: "",
  },
  person: {
    type: Object as Persons,
    default: {} as Persons,
  },
});

const emit = defineEmits(["update"]);

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
    <template #resume=""
      ><DivsResumeDiv
        :cand-id="props.candId"
        :editable="props.editable"
        :person="props.person"
        @update="emit('update')"
    /></template>
    <template #staff=""
      ><DivsStaffDiv :cand-id="props.candId" :editable="props.editable"
    /></template>
    <template #education=""
      ><DivsEducateDiv :cand-id="props.candId" :editable="props.editable"
    /></template>
    <template #work=""
      ><DivsWorkDiv :cand-id="props.candId" :editable="props.editable"
    /></template>
    <template #document=""
      ><DivsDocumDiv :cand-id="props.candId" :editable="props.editable"
    /></template>
    <template #address=""
      ><DivsAddressDiv :cand-id="props.candId" :editable="props.editable"
    /></template>
    <template #contact=""
      ><DivsContactDiv :cand-id="props.candId" :editable="props.editable"
    /></template>
    <template #affiliation=""
      ><DivsAffilDiv :cand-id="props.candId" :editable="props.editable"
    /></template>
    <template #prev=""
      ><DivsPrevDiv :cand-id="props.candId" :editable="props.editable"
    /></template>
    <template #relate=""
      ><DivsRelateDiv :cand-id="props.candId" :editable="props.editable"
    /></template>
  </UAccordion>
</template>
