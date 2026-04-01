<script setup lang="ts">
import type { Items } from "@/types";

const itemStore = useItemStore();

await callOnce(async () => await itemStore.getItems());
</script>

<template>
  <!-- Меню для переключения между вкладками -->
  <UTabs
    :items="tabsItems"
    :unmount-on-hide="false"
    variant="pill"
    class="mt-4"
  >
    <!-- Слот вкладки для отображения анкеты -->
    <template #anketa>
      <div class="mt-4">
        <ContentPersonView />
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
            :icon="accordion.icon"
            :view="accordion.slot as keyof Items"
            :title="accordion.label"
          />
        </template>
      </UAccordion>
    </template>

    <!-- Вкладки проверки, полиграф и др. -->
    <template v-for="tab in tabsItems.slice(1)" #[tab.slot] :key="tab.slot">
      <div class="mt-2">
        <ContentItemView
          :icon="tab.icon"
          :view="tab.slot as keyof Items"
          :title="tab.label"
        />
      </div>
    </template>
  </UTabs>
</template>
