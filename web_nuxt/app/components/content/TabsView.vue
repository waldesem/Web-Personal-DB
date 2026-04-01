<script setup lang="ts">
import type { Items } from "@/types";
import { accordion, tabs } from "@/utils";

const itemStore = useItemStore();

await callOnce(async () => await itemStore.getItems());
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
            :view="accord.slot as keyof Items"
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
          :view="tab.slot as keyof Items"
          :title="tab.label"
        />
      </div>
    </template>
  </UTabs>
</template>
