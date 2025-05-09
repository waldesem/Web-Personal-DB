<script setup lang="ts">
import type { AccordionItem } from "@nuxt/ui";

const emit = defineEmits(["update"]);

await preloadComponents(["DivsResumeDiv", "DivsSharedDiv"]);

const items: AccordionItem[] = [
  { content: "staffs", label: "Должности", icon: "i-heroicons-user" },
  {
    content: "educations",
    label: "Образование",
    icon: "i-heroicons-academic-cap",
  },
  {
    content: "workplaces",
    label: "Места работы",
    icon: "i-heroicons-briefcase",
  },
  {
    content: "documents",
    label: "Документы",
    icon: "i-heroicons-document-text",
  },
  {
    content: "addresses",
    label: "Адреса",
    icon: "i-heroicons-home-modern",
  },
  { content: "contacts", label: "Контакты", icon: "i-heroicons-phone" },
  {
    content: "previous",
    label: "Изменения имени",
    icon: "i-heroicons-pencil",
  },
  {
    content: "affilations",
    label: "Аффилированность",
    icon: "i-heroicons-user-group",
  },
];
</script>

<template>
  <DivsResumeDiv @update="emit('update')" />
  <UAccordion
    :items="items"
    :unmount-on-hide="false"
    :ui="{ item: 'border rounded-md' }"
    type="multiple"
  >
    <template #content="{ item }">
      <DivsSharedDiv :view="(item.content as string)" />
    </template>
  </UAccordion>
</template>
