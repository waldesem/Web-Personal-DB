<script setup lang="ts">
import type { Item, ItemKey, Items } from "@/types";

const props = defineProps({
  data: {
    type: Object as PropType<Items>,
    required: true,
  },
});

// Определяем массив элементов аккордеона
const items = [
  {
    content: "staffs",
    label: "Должности",
    icon: "i-lucide-workflow",
    slot: "staffs" as const,
    item: props.data.staffs,
    ItemComponent: resolveComponent("ItemsStaffItem"),
    FormComponent: resolveComponent("FormsStaffForm"),
  },
  {
    content: "educations",
    label: "Образование",
    icon: "i-lucide-graduation-cap",
    slot: "educations" as const,
    item: props.data.educations,
    ItemComponent: resolveComponent("ItemsEducationItem"),
    FormComponent: resolveComponent("FormsEducationForm"),
  },
  {
    content: "workplaces",
    label: "Места работы",
    icon: "i-lucide-briefcase-business",
    slot: "workplaces" as const,
    item: props.data.workplaces,
    ItemComponent: resolveComponent("ItemsWorkplaceItem"),
    FormComponent: resolveComponent("FormsWorkplaceForm"),
  },
  {
    content: "documents",
    label: "Документы",
    icon: "i-lucide-book-text",
    slot: "documents" as const,
    item: props.data.documents,
    ItemComponent: resolveComponent("ItemsDocumentItem"),
    FormComponent: resolveComponent("FormsDocumentForm"),
  },
  {
    content: "addresses",
    label: "Адреса",
    icon: "i-lucide-house",
    slot: "addresses" as const,
    item: props.data.addresses,
    ItemComponent: resolveComponent("ItemsAddressItem"),
    FormComponent: resolveComponent("FormsAddressForm"),
  },
  {
    content: "contacts",
    label: "Контакты",
    icon: "i-lucide-phone-call",
    slot: "contacts" as const,
    item: props.data.contacts,
    ItemComponent: resolveComponent("ItemsContactItem"),
    FormComponent: resolveComponent("FormsContactForm"),
  },
  {
    content: "previous",
    label: "Изменения имени",
    icon: "i-lucide-file-pen-line",
    slot: "previous" as const,
    item: props.data.previous,
    ItemComponent: resolveComponent("ItemsPreviousItem"),
    FormComponent: resolveComponent("FormsPreviousForm"),
  },
  {
    content: "affilations",
    label: "Аффилированность",
    icon: "i-lucide-users-round",
    slot: "affilations" as const,
    item: props.data.affilations,
    ItemComponent: resolveComponent("ItemsAffilationItem"),
    FormComponent: resolveComponent("FormsAffilationForm"),
  },
] as {
  content: ItemKey;
  label: string;
  icon: string;
  slot: string;
  item: Item[];
  ItemComponent: Component;
  FormComponent: Component;
}[];
</script>

<template>
  <!-- Выводим аккордеон с данными staffs, educations и т.д. -->
  <UAccordion :items="items" :unmount-on-hide="false">
    <template
      v-for="accord in items"
      #[accord.slot]="{ item }"
      :key="accord.slot"
    >
      <ContentItemView :icon="item.icon" :view="item.content" :data="item.item">
        <template
          v-for="index in item.item?.length"
          :key="index"
          #[`item-${item.content}-${index}`]="{ itemContent }"
        >
          <component
            :is="accord.ItemComponent"
            :item="(itemContent as object)"
          />
        </template>

        <template #[`form-${item.content}`]="{ formContent, submitItem }">
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
