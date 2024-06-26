<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount } from "vue";
import { stateUser, stateAnketa, stateAlert } from "@/state";
import { useRoute } from "vue-router";
import { server } from "@/utilities";
import { axiosAuth } from "@/auth";
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
  const route = useRoute();
  stateAnketa.share.candId = route.params.id as string;
  try {
      const response = await axiosAuth.get(
        `${server}/allinone/${stateAnketa.share.candId}`,
      );
      [
        stateAnketa.anketa.resume,
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

const tabsData = [
  ["AnketaTab", "Анкета", "person-vcard", AnketaTab],
  ["CheckTab", "Проверки", "journal-check", CheckTab],
  ["PoligrafTab", "Полиграф", "heart-pulse", PoligrafTab],
  ["InvestigateTab", "Расследования", "incognito", InvestigateTab],
  ["InquiryTab", "Запросы", "card-text", InquiryTab],
];
</script>

<template>
  <PhotoCard />
  <div class="row mb-3">
    <div class="col-md-10">
      <HeaderDiv
        :cls="'text-info py-3'"
        :page-header="`${stateAnketa.anketa.resume.surname} ${
          stateAnketa.anketa.resume.firstname
        } ${
          stateAnketa.anketa.resume.patronymic
            ? ' ' + stateAnketa.anketa.resume.patronymic
            : ''
        }`"
      />
    </div>
    <div class="col-md-2 d-flex justify-content-end d-print-none">
      <IconRelative
        :title="`Взять на проверку`"
        :icon-class="`bi bi-person-plus fs-1`"
        :hide="stateAnketa.anketa.resume.user_id == stateUser.userId"
        @onclick="stateAnketa.getResume('self')"
      />
      <IconRelative
        :title="`Версия для печати`"
        :icon-class="`bi bi-printer fs-1`"
      />
    </div>
  </div>
  <nav class="nav nav-tabs nav-justified" role="tablist">
    <button
      v-for="(tab, idx) in tabsData" :key="idx"
      class="nav-link"
      :class="{ active: idx === 0 }"
      :data-bs-target="`#${tab[0]}`"
      data-bs-toggle="tab"
      type="button"
      role="tab"
    >
      <i :class="`bi bi-${tab[2]}`"></i>
      {{ tab[1] }}
    </button>
  </nav>
  <div class="tab-content">
    <div v-for="(tab, idx) in tabsData" :key="idx"
      :id="`${tab[0]}`"
      class="tab-pane show fade mb-1 py-3"
      :class="{ active: idx === 0 }"
      role="tabpanel"
    >
      <component :is="tab[3]"></component>
    </div>
  </div>
</template>
