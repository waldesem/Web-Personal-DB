<script setup lang="ts">
import type { Items } from "@/types";

const { $api } = useNuxtApp();

const personId = inject("personId") as Ref<string>;

const { data } = await useAsyncData(
  "items",
  () => $api<Items>("/routes/items/" + personId.value),
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
          :data="data[tab.slot]"
          :icon="tab.icon"
          :view="tab.slot"
          :title="tab.label"
        />
      </div>
    </template>
  </UTabs>
</template>
