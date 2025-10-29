<script setup lang="ts">
definePageMeta({
  layout: false,
});

onMounted(() => window.print());

const { data: person } = useNuxtData("person");

const items = [
  {
    label: "Должности",
    component: resolveComponent("ItemsStaffItem"),
    data: useNuxtData("staffs").data.value,
  },
  {
    label: "Образование",
    component: resolveComponent("ItemsEducationItem"),
    data: useNuxtData("educations").data.value,
  },
  {
    label: "Места работы",
    component: resolveComponent("ItemsWorkplaceItem"),
    data: useNuxtData("workplaces").data.value,
  },
  {
    label: "Документы",
    component: resolveComponent("ItemsDocumentItem"),
    data: useNuxtData("documents").data.value,
  },
  {
    label: "Адреса",
    component: resolveComponent("ItemsAddressItem"),
    data: useNuxtData("addresses").data.value,
  },
  {
    label: "Контакты",
    component: resolveComponent("ItemsContactItem"),
    data: useNuxtData("contacts").data.value,
  },
  {
    label: "Изменения имени",
    component: resolveComponent("ItemsPreviousItem"),
    data: useNuxtData("previous").data.value,
  },
  {
    label: "Аффилированность",
    component: resolveComponent("ItemsAffilationItem"),
    data: useNuxtData("affilations").data.value,
  },
  {
    label: "Проверки",
    component: resolveComponent("ItemsCheckItem"),
    data: useNuxtData("checks").data.value,
  },
  {
    label: "Полиграф",
    component: resolveComponent("ItemsPoligrafItem"),
    data: useNuxtData("poligrafs").data.value,
  },
  {
    label: "Расследования",
    component: resolveComponent("ItemsInquestItem"),
    data: useNuxtData("investigations").data.value,
  },
  {
    label: "Запросы",
    component: resolveComponent("ItemsInquiryItem"),
    data: useNuxtData("inquiries").data.value,
  },
];
</script>

<template>
  <UMain>
    <UPage>
      <UPageHeader
        :title="`${person?.surname} ${person?.firstname} ${
          person?.patronymic ?? ''
        }`"
        :ui="{
          title: 'text-2xl sm:text-xl',
        }"
      />
      <ItemsPersonItem :item="person" />
      <div v-for="(item, index) in items" :key="index">
        <USeparator v-if="item.data" type="dashed" :label="item.label" />
        <div v-for="(data, idx) in item.data" :key="idx">
          <component :is="item.component" :item="data" />
          <USeparator
            v-if="idx + 1 !== item.data.length"
            type="dotted"
            label="#"
          />
        </div>
      </div>
    </UPage>
  </UMain>
</template>
