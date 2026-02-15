<script setup lang="ts">
import type { Items } from "@/types";

const candId = inject("candId") as Ref<string>;

const { $api } = useNuxtApp();

const { data } = await useAsyncData(
  "items",
  () => $api<Items>("/routes/items/" + candId.value),
  {
    default: () => ({} as Items),
  }
);

// Определяем массив элементов табов
const tabs = [
  {
    label: "Анкета",
    icon: "i-lucide-user",
    slot: "anketa" as const,
  },
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
const accordion = [
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
</script>

<template>
  <!-- Меню для переключения между вкладками -->
  <UTabs :items="tabs" :unmount-on-hide="false" variant="pill" class="mt-4">
    <!-- Слот вкладки для отображения анкеты -->
    <template #anketa>
      <div class="mt-4">
        <ContentPersonDiv />
      </div>
      <USeparator />
      <!-- Aккордеон с данными staffs, educations и т.д. -->
      <UAccordion :items="accordion" :unmount-on-hide="false">
        <template v-for="accord in accordion" #[accord.slot] :key="accord.slot">
          <ContentItemView
            :icon="accord.icon"
            :data="data[accord.slot]"
            :view="(accord.slot as keyof Items)"
            :title="accord.label"
          />
        </template>
      </UAccordion>
    </template>

    <!-- Вкладки проверки, полиграф и др. -->
    <template v-for="tab in tabs.slice(1)" #[tab.slot] :key="tab.slot">
      <div class="mt-2">
        <ContentItemView
          :icon="tab.icon"
          :data="data[tab.slot as keyof Items]"
          :view="(tab.slot as keyof Items)"
          :title="tab.label"
        />
      </div>
    </template>
  </UTabs>
</template>
