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
