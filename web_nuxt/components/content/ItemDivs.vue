<script setup lang="ts">
import type { Item } from "@/types";

// Определяем массив элементов аккордеона
const items = [
  {
    content: "staffs",
    label: "Должности",
    icon: "i-lucide-user",
    slot: "staffs" as const,
    ItemComponent: resolveComponent("ItemsStaffItem"),
    FormComponent: resolveComponent("FormsStaffForm"),
  },
  {
    content: "educations",
    label: "Образование",
    icon: "i-lucide-graduation-cap",
    slot: "educations" as const,
    ItemComponent: resolveComponent("ItemsEducationItem"),
    FormComponent: resolveComponent("FormsEducationForm"),
  },
  {
    content: "workplaces",
    label: "Места работы",
    icon: "i-lucide-briefcase-business",
    slot: "workplaces" as const,
    ItemComponent: resolveComponent("ItemsWorkplaceItem"),
    FormComponent: resolveComponent("FormsWorkplaceForm"),
  },
  {
    content: "documents",
    label: "Документы",
    icon: "i-lucide-book-text",
    slot: "documents" as const,
    ItemComponent: resolveComponent("ItemsDocumentItem"),
    FormComponent: resolveComponent("FormsDocumentForm"),
  },
  {
    content: "addresses",
    label: "Адреса",
    icon: "i-lucide-house",
    slot: "addresses" as const,
    ItemComponent: resolveComponent("ItemsAddressItem"),
    FormComponent: resolveComponent("FormsAddressForm"),
  },
  {
    content: "contacts",
    label: "Контакты",
    icon: "i-lucide-phone-call",
    slot: "contacts" as const,
    ItemComponent: resolveComponent("ItemsContactItem"),
    FormComponent: resolveComponent("FormsContactForm"),
  },
  {
    content: "previous",
    label: "Изменения имени",
    icon: "i-lucide-file-pen-line",
    slot: "previous" as const,
    ItemComponent: resolveComponent("ItemsPreviousItem"),
    FormComponent: resolveComponent("FormsPreviousForm"),
  },
  {
    content: "affilations",
    label: "Аффилированность",
    icon: "i-lucide-users-round",
    slot: "affilations" as const,
    ItemComponent: resolveComponent("ItemsAffilationItem"),
    FormComponent: resolveComponent("FormsAffilationForm"),
  },
];
</script>

<template>
  <!-- Выводим аккордеон с данными staffs, educations и т.д. -->
  <UAccordion :items="items" :unmount-on-hide="false">
    <template
      v-for="accord in items"
      #[accord.slot]="{ item }"
      :key="accord.slot"
    >
      <ContentItemView :icon="item.icon" :view="item.content">
        <template #item="{ itemContent }">
          <component
            :is="accord.ItemComponent"
            :item="(itemContent as Item)"
          />
        </template>

        <template #form="{ formContent, submitItem }">
          <component
            :is="accord.FormComponent"
            :item="(formContent as unknown as undefined)"
            @update="submitItem"
          />
        </template>
      </ContentItemView>
    </template>
  </UAccordion>
</template>
