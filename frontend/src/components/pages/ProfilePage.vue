<script setup lang="ts">
import { defineAsyncComponent, ref, onBeforeMount, provide } from "vue";
import { useRoute } from "vue-router";

const PhotoCard = defineAsyncComponent(
  () => import("@components/layouts/PhotoCard.vue")
);
const AnketaTab = defineAsyncComponent(
  () => import("@components/tabs/AnketaTab.vue")
);
const CheckTab = defineAsyncComponent(
  () => import("@components/tabs/CheckTab.vue")
);
const PoligrafTab = defineAsyncComponent(
  () => import("@components/tabs/PoligrafTab.vue")
);
const InvestigateTab = defineAsyncComponent(
  () => import("@components/tabs/InvestigateTab.vue")
);
const InquiryTab = defineAsyncComponent(
  () => import("@components/tabs/InquiryTab.vue")
);

const route = useRoute();

onBeforeMount(() => {
  dataProfile.value.candId = route.params.id.toString();
});

const dataProfile = ref({
  candId: route.params.id.toString()
});

provide("candId", dataProfile.value.candId);

const tabsObject = {
  anketaTab: ["Анкета", AnketaTab],
  сheckTab: ["Проверки", CheckTab],
  poligrafTab: ["Полиграф", PoligrafTab],
  investigateTab: ["Расследования", InvestigateTab],
  inquiryTab: ["Запросы", InquiryTab],
};

const printPage = ref(false);

</script>

<template>
  <div class="container py-3">
    <PhotoCard />
    <div v-if="!printPage" class="nav nav-tabs nav-justified" role="tablist">
      <button
        v-for="(value, key) in tabsObject"
        :key="key"
        class="nav-link"
        :class="{ active: key === 'anketaTab' }"
        data-bs-toggle="tab"
        :data-bs-target="`#${key}`"
        type="button"
        role="tab"
      >
        {{ value[0] }}
      </button>
    </div>

    <div v-if="!printPage" class="tab-content">
      <div
        v-for="(value, key) in tabsObject"
        :key="key"
        :id="key"
        class="tab-pane fade py-1"
        role="tabpanel"
        :class="{ ' show active': key === 'anketaTab' }"
      >
        <component :is="value[1]"></component>
      </div>
    </div>

    <div v-if="printPage">
      <div v-for="(value, key) in tabsObject" :key="key" :id="key">
        <component :is="value[1]"></component>
      </div>
    </div>

    <a href="#" class="d-print-none" @click="printPage = !printPage">
      <i class="bi bi-printer fs-1" title="Версия для печати"></i>
    </a>
  </div>
</template>

<style scoped>
.bi-printer {
  position: fixed;
  top: 80px;
  right: 40px;
  z-index: 9999;
  border-radius: 50%;
  padding: 10px;
  cursor: pointer;
}
</style>
