<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount } from "vue";
import { stateClassify, stateUser, stateAnketa } from "@/state";
import { router } from "@/router";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/content/elements/HeaderDiv.vue")
);
const IconRelative = defineAsyncComponent(
  () => import("@components/content/elements/IconRelative.vue")
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
  stateAnketa.share.candId = router.currentRoute.value.params.id.toString();
  await stateAnketa.getResume();
});

const tabData = [
  ["AnketaTab", "Анкета", AnketaTab],
  ["CheckTab", "Проверки", CheckTab],
  ["PoligrafTab", "Полиграф", PoligrafTab],
  ["InvestigateTab", "Расследования", InvestigateTab],
  ["InquiryTab", "Запросы", InquiryTab],
];
</script>

<template>
  <PhotoCard />
  <div class="row mb-3">
    <div class="col-md-10">
      <HeaderDiv
        :page-header="`${stateAnketa.anketa.resume.surname} ${stateAnketa.anketa.resume.firstname} ${stateAnketa.anketa.resume.patronymic}`"
      />
    </div>
    <div class="col-md-2 d-flex justify-content-end d-print-none">
      <IconRelative
        :title="`Версия для печати`"
        :icon-class="`bi bi-printer fs-1`"
        @click="stateAnketa.share.printPage = !stateAnketa.share.printPage"
      />
      <IconRelative
        :title="`Взять на проверку`"
        :icon-class="`bi bi-person-plus fs-1`"
        :hide="
          stateAnketa.anketa.resume.user_id !== null &&
          stateAnketa.anketa.resume.user_id !== ''
        "
        @onclick="stateAnketa.getResume('self')"
      />
      <IconRelative
        :title="`Отправить на проверку`"
        :icon-class="'bi bi-send-plus fs-1'"
        :hide="
          stateAnketa.anketa.resume.user_id !== stateUser.userId ||
          stateAnketa.anketa.resume.status_id === stateClassify.status['robot']
        "
        @onclick="stateAnketa.getResume('send')"
      >
      </IconRelative>
    </div>
  </div>
  <nav
    v-if="!stateAnketa.share.printPage"
    class="nav nav-tabs nav-justified"
    role="tablist"
  >
    <button
      v-for="(tab, idx) in tabData"
      :key="idx"
      class="nav-link"
      :class="{ active: idx === 0 }"
      :data-bs-target="`#${tab[0]}`"
      data-bs-toggle="tab"
      type="button"
      role="tab"
    >
      {{ tab[1] }}
    </button>
  </nav>
  <div
    v-for="(tab, idx) in tabData"
    :key="idx"
    :class="{ 'tab-content': !stateAnketa.share.printPage }"
  >
    <div
      class="py-3"
      :id="(tab[0] as string)"
      :class="{
        'tab-pane fade mb-1': !stateAnketa.share.printPage,
        'show active': idx === 0,
      }"
      role="tabpanel"
    >
      <component :is="tab[2]" />
    </div>
  </div>
</template>
