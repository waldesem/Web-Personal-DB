<script setup lang="ts">
import type { ItemKey, Items } from "@/types";

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
    ItemComponent: resolveComponent("LazyItemsCheckItem"),
    FormComponent: resolveComponent("LazyFormsCheckForm"),
  },
  {
    content: "poligrafs" as ItemKey,
    label: "Полиграф",
    icon: "i-lucide-heart-pulse",
    slot: "poligrafs" as const,
    item: data.value.poligrafs,
    ItemComponent: resolveComponent("LazyItemsPoligrafItem"),
    FormComponent: resolveComponent("LazyFormsPoligrafForm"),
  },
  {
    content: "investigations" as ItemKey,
    label: "Расследования",
    icon: "i-lucide-hat-glasses",
    slot: "investigations" as const,
    item: data.value.investigations,
    ItemComponent: resolveComponent("LazyItemsInquestItem"),
    FormComponent: resolveComponent("LazyFormsInquestForm"),
  },
  {
    content: "inquiries" as ItemKey,
    label: "Запросы",
    icon: "i-lucide-message-circle-question-mark",
    slot: "inquiries" as const,
    item: data.value.inquiries,
    ItemComponent: resolveComponent("LazyItemsInquiryItem"),
    FormComponent: resolveComponent("LazyFormsInquiryForm"),
  },
];
</script>

<template>
  <!-- Меню для переключения между вкладками -->
  <UTabs :items="items" variant="pill" class="mt-4">
    <!-- Слот вкладки для отображения анкеты -->
    <template #anketa>
      <div class="mt-4">
        <slot name="anketa-tab" />
      </div>
      <USeparator />
      <!-- Выводим аккордеон с данными staffs, educations и т.д. -->
      <ContentItemDivs :data="data" />
    </template>

    <!-- Вкладки проверки, полиграф и др. -->
    <template v-for="tab in items.slice(1)" #[tab.slot] :key="tab.content">
      <div class="mt-2">
        <ContentItemView :view="tab.content" :icon="tab.icon" :data="tab.item">
          <template
            v-for="index in tab.item?.length"
            :key="index"
            #[`item-${tab.content}-${index}`]="{ itemContent }"
          >
            <component
              :is="tab.ItemComponent"
              :item="(itemContent as object)"
            />
          </template>

          <template #[`form-${tab.content}`]="{ formContent, submitItem }">
            <component
              :is="tab.FormComponent"
              :item="(formContent as object)"
              @update="submitItem"
            />
          </template>
        </ContentItemView>
      </div>
    </template>
  </UTabs>
</template>
