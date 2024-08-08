<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { stateUser, stateAnketa, stateClassify, prefix } from "@/state";
import { useRoute } from "vue-router";
import { axiosAuth } from "@/auth";

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
const HeaderDiv = defineAsyncComponent(
  () => import("@components/content/elements/HeaderDiv.vue")
);
const PhotoCard = defineAsyncComponent(
  () => import("@components/content/divs//PhotoCard.vue")
);

onBeforeMount(async () => {
  const route = useRoute();
  stateAnketa.share.candId = route.params.id as string;
  try {
    const response = await axiosAuth.get(
      `${prefix}/profile/${stateAnketa.share.candId}`
    );
    const resp = response.data;
    const anketaKeys = Object.keys(stateAnketa.anketa);
    for (let i = 0; i < anketaKeys.length; i++) {
      stateAnketa.anketa[anketaKeys[i] as keyof typeof stateAnketa.anketa] =
        resp[i];
    }
    stateAnketa.getImage();
  } catch (error: any) {
    console.error(error);
  }
});

const currentTab = ref("anketaTab");

const tabsData = {
  anketaTab: ["Взять анкету", "Анкета", AnketaTab,],
  checkTab: ["Добавить проверку", "Проверки", CheckTab, "bi-person-check"],
  poligrafTab: ["Добавить полиграф", "Полиграф", PoligrafTab, "bi-heart-pulse"],
  investigateTab: ["Добавить расследования", "Расследования", InvestigateTab, "bi-incognito"],
  inquiryTab: ["Добавить запрос", "Запросы", InquiryTab, "bi-journal-check"],
};

async function closeCollapses() {
  const collapseCollection = document.getElementsByClassName("collapse");
  for (let i = 0; i < collapseCollection.length; i++) {
    collapseCollection[i]?.setAttribute(
      "class",
      "collapse card card-body mb-3"
    );
  }
}

async function switchStandings() {
  await closeCollapses();
  stateAnketa.getItem("persons", "self");
}

async function switchTabs(tab: string) {
  await closeCollapses();
  currentTab.value = tab;
}
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
    <div 
      v-if="stateUser.user.role == stateClassify.classes.roles['user']"
      class="col-md-2 d-flex justify-content-end d-print-none"
    >
      <div
        v-for="(item, idx) in Object.keys(tabsData).slice(1)"
        :key="idx"
        class="position-relative"
      >
        <div
          v-if="
            currentTab == item &&
            stateAnketa.anketa.persons['user_id'] == stateUser.user.userId &&
            stateAnketa.anketa.persons['standing']
          "
          :title="(tabsData[currentTab as keyof typeof tabsData][0] as string)"
          class="text-danger fs-1"
          style="cursor: pointer"
          data-bs-toggle="collapse"
          :href="'#clps_' + item.split('T')[0]"
        >
        <i class="bi" :class="tabsData[currentTab as keyof typeof tabsData][3]"></i>
        </div>
      </div>
      <div v-if="currentTab == 'anketaTab'" class="position-relative">
        <button
          type="button"
          :class="
            stateAnketa.anketa.persons['standing']
              ? 'btn btn-link'
              : 'btn btn-outline-danger'
          "
          :title="
            stateAnketa.anketa.persons['standing']
              ? 'Отключить режим проверки'
              : 'Включить режим проверки'
          "
          @click="switchStandings"
        >
          <span
            v-if="stateAnketa.anketa.persons['standing']"
            class="spinner-grow text-danger"
            role="status"
          >
          </span>
          <div class="text-danger fs-5" v-else><i class="bi bi-pencil-square"></i>
          </div>
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
      @click="switchTabs(key)"
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
  .card,
  .card-body {
    border: none !important;
  }
}
</style>
