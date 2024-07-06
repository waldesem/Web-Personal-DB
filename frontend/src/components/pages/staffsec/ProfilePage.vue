<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { stateUser, stateAnketa, server } from "@/state";
import { useRoute } from "vue-router";
import { axiosAuth } from "@/auth";

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

onBeforeMount(async () => {
  const route = useRoute();
  stateAnketa.share.candId = route.params.id as string;
  try {
    const response = await axiosAuth.get(
      `${server}/profile/${stateAnketa.share.candId}`
    );
    [
      stateAnketa.anketa.persons,
      stateAnketa.anketa.previous,
      stateAnketa.anketa.staffs,
      stateAnketa.anketa.documents,
      stateAnketa.anketa.addresses,
      stateAnketa.anketa.contacts,
      stateAnketa.anketa.educations,
      stateAnketa.anketa.workplaces,
      stateAnketa.anketa.affilations,
      stateAnketa.anketa.relations,
      stateAnketa.anketa.checks,
      stateAnketa.anketa.investigations,
      stateAnketa.anketa.poligrafs,
      stateAnketa.anketa.inquiries,
    ] = response.data;
  } catch (error: any) {
    console.error(error);
  }
});

const currentTab = ref("anketaTab");

const tabsData = {
  anketaTab: ["Взять анкету", "Анкета", AnketaTab],
  checkTab: ["Добавить проверку", "Проверки", CheckTab],
  poligrafTab: ["Добавить полиграф", "Полиграф", PoligrafTab],
  investigateTab: ["Добавить расследования", "Расследования", InvestigateTab],
  inquiryTab: ["Добавить запрос", "Запросы", InquiryTab],
};
</script>

<template>
  <PhotoCard />
  <div class="row mb-3">
    <div class="col-md-10">
      <HeaderDiv
        :cls="'text-danger py-3'"
        :page-header="`${stateAnketa.anketa.persons.surname} ${
          stateAnketa.anketa.persons.firstname
        } ${
          stateAnketa.anketa.persons.patronymic
            ? ' ' + stateAnketa.anketa.persons.patronymic
            : ''
        }`"
      />
    </div>
    <div class="col-md-2 d-flex justify-content-end d-print-none">
      <div
        v-if="
          currentTab === 'anketaTab' &&
          stateAnketa.anketa.persons['user_id'] != stateUser.userId
        "
        class="position-relative text-end"
      >
        <button
          type="button"
          class="btn btn-lg btn-outline-danger"
          :title="'Назначить анкету себе'"
          @click="stateAnketa.getItem('persons', 'self')"
        >
          &equiv;
        </button>
      </div>
      <div
        v-for="(item, idx) in Object.keys(tabsData).slice(1)"
        :key="idx"
        class="position-relative text-end"
      >
        <button
          v-if="
            currentTab == item &&
            stateAnketa.anketa.persons['user_id'] == stateUser.userId
          "
          :title="(tabsData[currentTab as keyof typeof tabsData][0] as string)"
          type="button"
          class="btn btn-lg btn-outline-danger"
          data-bs-toggle="collapse"
          :href="'#clps_' + item.split('T')[0]"
        >
          &equiv;
        </button>
      </div>
    </div>
  </div>
  <nav class="nav nav-tabs nav-justified d-print-none" role="tablist">
    <button
      v-for="(values, key) in tabsData"
      :key="key"
      class="nav-link"
      :class="{ active: key === 'anketaTab' }"
      :data-bs-target="'#' + key"
      data-bs-toggle="tab"
      type="button"
      role="tab"
      @click="currentTab = key"
    >
      {{ values[1] }}
    </button>
  </nav>
  <div class="tab-content">
    <div
      v-for="(values, key) in tabsData"
      :key="key"
      :id="key"
      class="tab-pane show fade pt-3"
      :class="{ active: key == 'anketaTab' }"
      role="tabpanel"
    >
      <component :is="values[2]"></component>
    </div>
  </div>
</template>

<style>
@media print {
  .tab-content > .tab-pane {
    display: block;
  }
  .tab-pane {
    padding-top: 1px !important;
  }
  .card, .card-body {
    border: none !important;
  }
}
</style>
