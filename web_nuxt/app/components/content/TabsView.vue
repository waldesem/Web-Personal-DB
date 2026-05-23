<script setup lang="ts">
import { anketaTab, itemsAccordion, itemsTabs } from "@/schema/elements";
import { itemsFields } from "@/schema/items";
import type { Items, Person } from "@/types";
import type { PropType } from "vue";

const { $api } = useNuxtApp();

const props = defineProps({
  person: {
    type: Object as PropType<Person>,
    required: true,
  },
});

const { data, pending } = await useAsyncData(
  "items",
  () => $api<Items>("/routes/items/" + props.person.id),
  { default: () => ({}) as Items },
);
</script>

<template>
  <!-- Меню для переключения между вкладками -->
  <UTabs
    :items="[anketaTab, ...itemsTabs]"
    :unmount-on-hide="false"
    variant="pill"
  >
    <!-- Слот вкладки для отображения анкеты -->
    <template #person>
      <ElementSkeletDivs v-if="pending" :rows="itemsFields.person.length" />
      <ContentPersonView v-else :person="props.person" />

      <USeparator />

      <!-- Aккордеон с данными staffs, educations и т.д. -->
      <UAccordion :items="itemsAccordion" :unmount-on-hide="false">
        <template
          v-for="accordion in itemsAccordion"
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
    <template v-for="tab in itemsTabs" #[tab.slot] :key="tab.slot">
      <ContentItemView
        :person-id="props.person.id"
        :data="data[tab.slot]"
        :icon="tab.icon"
        :view="tab.slot"
        :title="tab.label"
      />
    </template>
  </UTabs>
</template>
