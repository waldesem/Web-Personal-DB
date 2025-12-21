<script setup lang="ts">
import type { Item, ItemKey, Items } from "@/types";

const { $api } = useNuxtApp();

// Используем плагин для передачи данных на сервер
const candId = inject("candId") as Ref<string>;

const { data } = await useAsyncData(
  "items",
  () => $api<Items>("/routes/items/" + candId.value),
  { default: () => ({} as Items) }
);

// Определяем массив элементов табов
const items = [
  {
    content: "person" as ItemKey,
    label: "Анкета",
    icon: "i-lucide-user",
    slot: "anketa" as const,
  },
  {
    content: "checks" as ItemKey,
    label: "Проверки",
    icon: "i-lucide-shield-check",
    slot: "checks" as const,
    item: data.value.checks,
    ItemComponent: resolveComponent("ItemsCheckItem"),
    FormComponent: resolveComponent("LazyFormsCheckForm"),
  },
  {
    content: "poligrafs" as ItemKey,
    label: "Полиграф",
    icon: "i-lucide-heart-pulse",
    slot: "poligrafs" as const,
    item: data.value.poligrafs,
    ItemComponent: resolveComponent("ItemsPoligrafItem"),
    FormComponent: resolveComponent("LazyFormsPoligrafForm"),
  },
  {
    content: "investigations" as ItemKey,
    label: "Расследования",
    icon: "i-lucide-hat-glasses",
    slot: "investigations" as const,
    item: data.value.investigations,
    ItemComponent: resolveComponent("ItemsInquestItem"),
    FormComponent: resolveComponent("LazyFormsInquestForm"),
  },
  {
    content: "inquiries" as ItemKey,
    label: "Запросы",
    icon: "i-lucide-message-circle-question-mark",
    slot: "inquiries" as const,
    item: data.value.inquiries,
    ItemComponent: resolveComponent("ItemsInquiryItem"),
    FormComponent: resolveComponent("LazyFormsInquiryForm"),
  },
];
</script>

<template>
  <!-- Меню для переключения между вкладками -->
  <UTabs :items="items" variant="pill">
    <!-- Слот вкладки для отображения анкеты -->
    <template #anketa>
      <slot name="anketa-tab" />
      <USeparator />
      <!-- Выводим аккордеон с данными staffs, educations и т.д. -->
      <ContentItemDivs :data="data" />
    </template>

    <!-- Вкладки проверки, полиграф и др. -->
    <template v-for="tab in items.slice(1)" #[tab.slot] :key="tab.content">
      <ContentItemView :view="tab.content" :icon="tab.icon" :data="tab.item">
        <template #item="{ itemContent }">
          <component :is="tab.ItemComponent" :item="(itemContent as Item)" />
        </template>

        <template #form="{ formContent, submitItem }">
          <component
            :is="tab.FormComponent"
            :item="(formContent as unknown as undefined)"
            @update="submitItem"
          />
        </template>
      </ContentItemView>
    </template>
  </UTabs>
</template>
