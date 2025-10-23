<script setup lang="ts">
// Определяем массив элементов табов
const items = [
  {
    content: "person",
    label: "Анкета",
    icon: "i-lucide-user",
    slot: "anketa" as const,
  },
  {
    content: "checks",
    label: "Проверки",
    icon: "i-lucide-circle-check-big",
    slot: "checks" as const,
    ItemComponent: resolveComponent("ItemsCheckItem"),
    FormComponent: resolveComponent("FormsCheckForm"),
  },
  {
    content: "poligrafs",
    label: "Полиграф",
    icon: "i-lucide-heart-pulse",
    slot: "poligrafs" as const,
    ItemComponent: resolveComponent("ItemsPoligrafItem"),
    FormComponent: resolveComponent("FormsPoligrafForm"),
  },
  {
    content: "investigations",
    label: "Расследования",
    icon: "i-lucide-briefcase-business",
    slot: "investigations" as const,
    ItemComponent: resolveComponent("ItemsInquestItem"),
    FormComponent: resolveComponent("FormsInquestForm"),
  },
  {
    content: "inquiries",
    label: "Запросы",
    icon: "i-lucide-book-text",
    slot: "inquiries" as const,
    ItemComponent: resolveComponent("ItemsInquiryItem"),
    FormComponent: resolveComponent("FormsInquiryForm"),
  },
];
</script>

<template>
  <!-- Меню для переключения между вкладками -->
    <UTabs
      :unmount-on-hide="false"
      :ui="{ trigger: 'flex-1' }"
      :items="items"
      color="info"
      variant="pill"
      class="gap-4 w-full"
    >
      <!-- Слот вкладки для отображения анкеты -->
      <template #anketa>
        <slot name="anketa-tab" />
      </template>

      <!-- Вкладки проверки, полиграф и др. -->
      <template
        v-for="tab in items.slice(1)"
        #[tab.slot]="{ item }"
        :key="tab.slot"
      >
        <ContentSharedView :view="item.content">
          <template #item="{ itemContent }">
            <component
              :is="tab.ItemComponent"
              :v-bind="(itemContent as unknown as undefined)"
            />
          </template>

          <template #form="{ formContent, submitItem }">
            <component
              :is="tab.FormComponent"
              :item="(formContent as unknown as undefined)"
              @update="submitItem"
            />
          </template>
        </ContentSharedView>
      </template>
    </UTabs>
</template>