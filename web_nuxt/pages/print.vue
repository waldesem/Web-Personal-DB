<script setup lang="ts">
const { data: person } = useNuxtData('person');

const items = [
  {
    content: "staffs",
    label: "Должности",
    icon: "i-lucide-user",
    component: resolveComponent("ItemsStaffItem"),
  },
  {
    content: "educations",
    label: "Образование",
    icon: "i-lucide-graduation-cap",
    component: resolveComponent("ItemsEducationItem"),
  },
  {
    content: "workplaces",
    label: "Места работы",
    icon: "i-lucide-briefcase-business",
    component: resolveComponent("ItemsWorkplaceItem"),
  },
  {
    content: "documents",
    label: "Документы",
    icon: "i-lucide-book-text",
    component: resolveComponent("ItemsDocumentItem"),
  },
  {
    content: "addresses",
    label: "Адреса",
    icon: "i-lucide-house",
    component: resolveComponent("ItemsAddressItem"),
  },
  {
    content: "contacts",
    label: "Контакты",
    icon: "i-lucide-phone-call",
    component: resolveComponent("ItemsContactItem"),
  },
  {
    content: "previous",
    label: "Изменения имени",
    icon: "i-lucide-file-pen-line",
    component: resolveComponent("ItemsPreviousItem"),
  },
  {
    content: "affilations",
    label: "Аффилированность",
    icon: "i-lucide-users-round",
    component: resolveComponent("ItemsAffilationItem"),
  },
  {
    content: "checks",
    label: "Проверки",
    icon: "i-lucide-circle-check-big",
    component: resolveComponent("ItemsCheckItem"),
  },
  {
    content: "poligrafs",
    label: "Полиграф",
    icon: "i-lucide-heart-pulse",
    component: resolveComponent("ItemsPoligrafItem"),
  },
  {
    content: "investigations",
    label: "Расследования",
    icon: "i-lucide-briefcase-business",
    component: resolveComponent("ItemsInquestItem"),
  },
  {
    content: "inquiries",
    label: "Запросы",
    icon: "i-lucide-book-text",
    component: resolveComponent("ItemsInquiryItem"),
  },
];
</script>

<template>
  <Upage>
    <UPageCard title="Анкета" icon="i-lucide-user">
      <ItemsPersonItem :item="person" />
    </UPageCard>
    <UPageCard v-for="item in items" :key="item.content" :title="item.label">
      <div v-for="content in useNuxtData(item.content).data" :key="content.id">
        <component :is="item.component" :item="content"/>
      </div>
    </UPageCard>
  </Upage>
</template>
