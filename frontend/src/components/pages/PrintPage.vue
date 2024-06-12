<script setup lang="ts">
import { defineAsyncComponent } from "vue";
import { stateAnketa } from "@/state";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/content/elements/HeaderDiv.vue")
);
const PhotoCard = defineAsyncComponent(
  () => import("@components/content/divs//PhotoCard.vue")
);
const AnketaTab = defineAsyncComponent(
  () => import("@components/content/tabs/AnketaTab.vue")
);
const CheckTab = defineAsyncComponent(
  () => import("@components/content/tabs/CheckTab.vue")
);
const PoligrafTab = defineAsyncComponent(
  () => import("@components/content/tabs/PoligrafTab.vue")
);
const InvestigateTab = defineAsyncComponent(
  () => import("@components/content/tabs/InvestigateTab.vue")
);
const InquiryTab = defineAsyncComponent(
  () => import("@components/content/tabs/InquiryTab.vue")
);

const tabsData = ({
  tabs: [
    ["Анкета", AnketaTab],
    ["Проверки", CheckTab],
    ["Полиграф", PoligrafTab],
    ["Расследования", InvestigateTab],
    ["Запросы", InquiryTab],
  ],
});
</script>

<template>
  <div class="container-fluid">
    <PhotoCard />
    <HeaderDiv
      :cls="'text-info py-3'"
      :page-header="`${stateAnketa.anketa.resume.surname} ${stateAnketa.anketa.resume.firstname} ${stateAnketa.anketa.resume.patronymic}`"
    />
    <div
      v-for="(item, idx) in tabsData.tabs"
      :key="idx"
    >
      <div class="d-flex justify-content-between align-items-center mt-3">
        <p class="fs-5 fw-bold text-info">{{ (item[0] as string) }}</p>
      </div>
      <component :is="item[1]" />
    </div>
  </div>
</template>
