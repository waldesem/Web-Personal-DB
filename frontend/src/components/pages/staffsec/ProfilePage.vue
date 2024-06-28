<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { stateUser, stateAnketa, stateAlert } from "@/state";
import { useRoute } from "vue-router";
import { server } from "@/utilities";
import { axiosAuth } from "@/auth";
import { router } from "@/router";

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
    if (error.request.status == 401 || error.request.status == 403) {
      router.push({ name: "login" });
    } else {
      console.error(error);
      stateAlert.setAlert("alert-danger", `Ошибка: ${error}`);
    }
  }
});

const currentTab = ref("anketaTab");

const tabsData = [
  ["anketa", "Взять анкету", "Анкета", AnketaTab],
  ["check", "Добавить проверку", "Проверки", CheckTab],
  ["poligraf", "Добавить полиграф", "Полиграф", PoligrafTab],
  ["investigate", "Добавить расследования", "Расследования", InvestigateTab],
  ["inquiry", "Добавить запрос", "Запросы", InquiryTab],
];
</script>

<template>
  <PhotoCard />
  <div class="row mb-3">
    <div class="col-md-10">
      <HeaderDiv
        :cls="'text-info py-3'"
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
        v-show="currentTab == tabsData[0][0] + 'Tab'"
        class="position-relative text-end flex-grow-1"
      >
        <button
          type="button"
          class="btn btn-lg btn-outline-info"
          :title="'Взять анкету'"
          @click="stateAnketa.getItem('persons', 'self')"
          :disabled="stateAnketa.anketa.persons.user_id == stateUser.userId"
        >
          &equiv;
        </button>
      </div>
      <div 
        v-show="currentTab == value[0] + 'Tab'"
        v-for="(value, idx) in tabsData.slice(1)" :key="idx"
        class="position-relative text-end flex-grow-1"
      >
        <button
          :title="(value[1] as string)"
          type="button"
          class="btn btn-lg btn-outline-info"
          :disabled="stateAnketa.anketa.persons['user_id'] != stateUser.userId"
          data-bs-toggle="collapse"
          :href="`#${(value[0] as string)}`"
        >
          &equiv;
        </button>
      </div>
    </div>
  </div>
  <nav class="nav nav-tabs nav-justified" role="tablist">
    <button
      v-for="(values, idx) in tabsData"
      :key="idx"
      class="nav-link"
      :class="{ active: values[0] == tabsData[0][0] }"
      :data-bs-target="`#${tabsData[idx][0]}Tab`"
      data-bs-toggle="tab"
      type="button"
      role="tab"
      @click="currentTab = tabsData[idx][0] + 'Tab'"
    >
      {{ values[2] }}
    </button>
  </nav>
  <div class="tab-content">
    <div
      v-for="(values, idx) in tabsData"
      :key="idx"
      :id="tabsData[idx][0] + 'Tab'"
      class="tab-pane show fade pt-3"
      :class="{ active: values[0] == tabsData[0][0] }"
      role="tabpanel"
    >
      <component :is="values[4]"></component>
    </div>
  </div>
</template>

<style scoped>
@media print {
  .tab-content > .tab-pane {
    display: block;
  }
  .tab-pane {
    padding-top: 1px !important;
  }
}
</style>
