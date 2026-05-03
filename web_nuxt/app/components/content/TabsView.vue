<script setup lang="ts">
import type { Items, Person } from "@/types";
import type { PropType } from "vue";

const { $api } = useNuxtApp();

const props = defineProps({
  person: {
    type: Object as PropType<Person>,
    required: true,
  },
});

const tabAnketa = [
  {
    label: "Анкета",
    icon: "i-lucide-user",
    slot: "anketa" as const,
  },
];

// Определяем массив элементов табов
const tabsItems = [
  {
    label: "Проверки",
    icon: "i-lucide-shield-check",
    slot: "checks" as keyof Items,
  },
  {
    label: "Полиграф",
    icon: "i-lucide-heart-pulse",
    slot: "poligrafs" as keyof Items,
  },
  {
    label: "Расследования",
    icon: "i-lucide-hat-glasses",
    slot: "investigations" as keyof Items,
  },
  {
    label: "Запросы",
    icon: "i-lucide-file-question-mark",
    slot: "inquiries" as keyof Items,
  },
];

// Определяем массив элементов аккордеона
const accordionItems = [
  {
    label: "Должности",
    icon: "i-lucide-workflow",
    slot: "staffs" as keyof Items,
  },
  {
    label: "Образование",
    icon: "i-lucide-graduation-cap",
    slot: "educations" as keyof Items,
  },
  {
    label: "Места работы",
    icon: "i-lucide-briefcase-business",
    slot: "workplaces" as keyof Items,
  },
  {
    label: "Документы",
    icon: "i-lucide-book-text",
    slot: "documents" as keyof Items,
  },
  {
    label: "Адреса",
    icon: "i-lucide-house",
    slot: "addresses" as keyof Items,
  },
  {
    label: "Контакты",
    icon: "i-lucide-phone-call",
    slot: "contacts" as keyof Items,
  },
  {
    label: "Изменения имени",
    icon: "i-lucide-file-pen-line",
    slot: "previous" as keyof Items,
  },
  {
    label: "Аффилированность",
    icon: "i-lucide-users-round",
    slot: "affilations" as keyof Items,
  },
];

const { data } = await useAsyncData(
  "items",
  () => $api<Items>("/routes/items/" + props.person.id),
  { default: () => ({}) as Items },
);
</script>

<template>
  <!-- Меню для переключения между вкладками -->
  <UTabs
    :items="[...tabAnketa, ...tabsItems]"
    :unmount-on-hide="false"
    variant="pill"
    class="mt-4"
  >
    <!-- Слот вкладки для отображения анкеты -->
    <template #anketa>
      <div class="mt-4">
        <ContentPersonView :person="props.person" />
      </div>
      <USeparator />
      <!-- Aккордеон с данными staffs, educations и т.д. -->
      <UAccordion :items="accordionItems" :unmount-on-hide="false">
        <template
          v-for="accordion in accordionItems"
          #[accordion.slot]
          :key="accordion.slot"
        >
          <ContentItemView
            :person-id="props.person.id"
            :data="data[accordion.slot]"
            :icon="accordion.icon"
            :view="accordion.slot"
            :title="accordion.label"
          />
        </template>
      </UAccordion>
    </template>

    <!-- Вкладки проверки, полиграф и др. -->
    <template v-for="tab in tabsItems" #[tab.slot] :key="tab.slot">
      <div class="mt-2">
        <ContentItemView
          :person-id="props.person.id"
          :data="data[tab.slot]"
          :icon="tab.icon"
          :view="tab.slot"
          :title="tab.label"
        />
      </div>
    </template>
  </UTabs>
</template>
