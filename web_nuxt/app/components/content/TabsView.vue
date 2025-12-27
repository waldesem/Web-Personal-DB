<script setup lang="ts">
import type { ItemKey, Items } from "@/types";

const candId = inject("candId") as Ref<string>;

const { $api } = useNuxtApp();

const { data } = await useAsyncData(
  "items",
  () => $api<Items>("/routes/items/" + candId.value),
  { default: () => ({} as Items) }
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
    slot: "checks" as const,
  },
  {
    label: "Полиграф",
    icon: "i-lucide-heart-pulse",
    slot: "poligrafs" as const,
  },
  {
    label: "Расследования",
    icon: "i-lucide-hat-glasses",
    slot: "investigations" as const,
  },
  {
    label: "Запросы",
    icon: "i-lucide-message-circle-question-mark",
    slot: "inquiries" as const,
  },
];

// Определяем массив элементов аккордеона
const accordion = [
  {
    label: "Должности",
    icon: "i-lucide-workflow",
    slot: "staffs" as const,
  },
  {
    label: "Образование",
    icon: "i-lucide-graduation-cap",
    slot: "educations" as const,
  },
  {
    label: "Места работы",
    icon: "i-lucide-briefcase-business",
    slot: "workplaces" as const,
  },
  {
    label: "Документы",
    icon: "i-lucide-book-text",
    slot: "documents" as const,
  },
  {
    label: "Адреса",
    icon: "i-lucide-house",
    slot: "addresses" as const,
  },
  {
    label: "Контакты",
    icon: "i-lucide-phone-call",
    slot: "contacts" as const,
  },
  {
    label: "Изменения имени",
    icon: "i-lucide-file-pen-line",
    slot: "previous" as const,
  },
  {
    label: "Аффилированность",
    icon: "i-lucide-users-round",
    slot: "affilations" as const,
  },
];
</script>

<template>
  <!-- Меню для переключения между вкладками -->
  <UTabs :items="tabs" :unmount-on-hide="false" variant="pill" class="mt-4">
    <!-- Слот вкладки для отображения анкеты -->
    <template #anketa>
      <div class="mt-4">
        <ContentPersonView />
      </div>
      <USeparator />
      <!-- Aккордеон с данными staffs, educations и т.д. -->
      <UAccordion :items="accordion" :unmount-on-hide="false">
        <template v-for="accord in accordion" #[accord.slot] :key="accord.slot">
          <ContentItemView
            :icon="accord.icon"
            :data="data[accord.slot]"
            :view="accord.slot as ItemKey"
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
          :data="data[tab.slot as ItemKey]"
          :view="tab.slot as ItemKey"
          :title="tab.label"
        />
      </div>
    </template>
  </UTabs>
</template>
