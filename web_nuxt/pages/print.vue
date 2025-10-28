<script setup lang="ts">
import type { Person } from '@/types';

const items = [
  {
    content: "staffs",
    label: "Должности",
    icon: "i-lucide-user",
    slot: "staffs" as const,
    component: resolveComponent("ItemsStaffItem"),
  },
  {
    content: "educations",
    label: "Образование",
    icon: "i-lucide-graduation-cap",
    slot: "educations" as const,
    component: resolveComponent("ItemsEducationItem"),
  },
  {
    content: "workplaces",
    label: "Места работы",
    icon: "i-lucide-briefcase-business",
    slot: "workplaces" as const,
    component: resolveComponent("ItemsWorkplaceItem"),
  },
  {
    content: "documents",
    label: "Документы",
    icon: "i-lucide-book-text",
    slot: "documents" as const,
    component: resolveComponent("ItemsDocumentItem"),
  },
  {
    content: "addresses",
    label: "Адреса",
    icon: "i-lucide-house",
    slot: "addresses" as const,
    component: resolveComponent("ItemsAddressItem"),
  },
  {
    content: "contacts",
    label: "Контакты",
    icon: "i-lucide-phone-call",
    slot: "contacts" as const,
    component: resolveComponent("ItemsContactItem"),
  },
  {
    content: "previous",
    label: "Изменения имени",
    icon: "i-lucide-file-pen-line",
    slot: "previous" as const,
    component: resolveComponent("ItemsPreviousItem"),
  },
  {
    content: "affilations",
    label: "Аффилированность",
    icon: "i-lucide-users-round",
    slot: "affilations" as const,
    component: resolveComponent("ItemsAffilationItem"),
  },
  {
    content: "checks",
    label: "Проверки",
    icon: "i-lucide-circle-check-big",
    slot: "checks" as const,
    component: resolveComponent("ItemsCheckItem"),
  },
  {
    content: "poligrafs",
    label: "Полиграф",
    icon: "i-lucide-heart-pulse",
    slot: "poligrafs" as const,
    component: resolveComponent("ItemsPoligrafItem"),
  },
  {
    content: "investigations",
    label: "Расследования",
    icon: "i-lucide-briefcase-business",
    slot: "investigations" as const,
    component: resolveComponent("ItemsInquestItem"),
  },
  {
    content: "inquiries",
    label: "Запросы",
    icon: "i-lucide-book-text",
    slot: "inquiries" as const,
    component: resolveComponent("ItemsInquiryItem"),
  },
];
</script>

<template>
  <Upage>
    <UPageCard title="Анкета" icon="i-lucide-user">
      <ItemsPersonItem :item="useNuxtData('person').data as Person" />
    </UPageCard>
    <UPageCard v-for="item in items" :key="item.content" :title="item.label">
      <component :is="item.component" :item="useNuxtData(item.content).data" />
    </UPageCard>
  </Upage>
</template>
