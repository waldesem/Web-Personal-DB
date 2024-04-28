<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
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
const RobotTab = defineAsyncComponent(
  () => import("@components/content/tabs/RobotTab.vue")
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
const OneSTab = defineAsyncComponent(
  () => import("@components/content/tabs/OneSTab.vue")
);

onBeforeMount(async () => {
  stateAnketa.share.candId = router.currentRoute.value.params.id.toString();
  await stateAnketa.getResume();
});

const tabsData = ref({
  tabs: [
    ["AnketaTab", "Анкета", AnketaTab,],
    ["CheckTab", "Проверки", CheckTab],
    ["RobotTab", "Робот", RobotTab],
    ["PoligrafTab", "Полиграф", PoligrafTab],
    ["InvestigateTab", "Расследования", InvestigateTab],
    ["InquiryTab", "Запросы", InquiryTab],
    ["OneSTab", "1С", OneSTab],
  ],
  currentTab: "AnketaTab",
  tabAction: "",
});
</script>

<template>
  <PhotoCard/>
  <div class="row mb-3">
    <div class="col-md-10">
      <HeaderDiv
        :cls="'text-info py-3'"
        :page-header="`${stateAnketa.anketa.resume.surname} ${stateAnketa.anketa.resume.firstname} ${stateAnketa.anketa.resume.patronymic}`"
      />
    </div>
    <div class="col-md-2 d-flex justify-content-end">
      <IconRelative
        v-show="tabsData.currentTab == 'AnketaTab'"
        :title="`Взять на проверку`"
        :icon-class="`bi bi-arrow-clockwise fs-1`"
        :hide="stateAnketa.anketa.resume.user_id !== stateUser.userId"
        @onclick="stateAnketa.getResume('status')"
      />
      <IconRelative
        v-show="tabsData.currentTab == 'AnketaTab'"
        :title="`Взять на проверку`"
        :icon-class="`bi bi-person-plus fs-1`"
        :hide="stateAnketa.anketa.resume.user_id === stateUser.userId"
        @onclick="stateAnketa.getResume('self')"
      />
      <IconRelative 
        v-show="tabsData.currentTab == 'CheckTab'"
        :title="`Добавить проверку`"
        :icon-class="`bi bi-journal-check fs-1`"
        :hide="
          ![
            stateClassify.status['update'],
            stateClassify.status['save'],
            stateClassify.status['repeat'],
            stateClassify.status['manual'],
          ].includes(stateAnketa.anketa.resume['status_id']) &&
          stateAnketa.anketa.resume['user_id'] != stateUser.userId
        "
        @onclick="tabsData.tabAction = tabsData.tabAction ? '' : 'create';"
      />
      <IconRelative
        v-show="tabsData.currentTab == 'RobotTab'"
        :title="`Отправить на проверку`"
        :icon-class="'bi bi-send-plus fs-1'"
        :hide="stateAnketa.anketa.resume.user_id !== stateUser.userId"
        @onclick="stateAnketa.getResume('send')"
      />
      <IconRelative 
        v-show="tabsData.currentTab == 'PoligrafTab'"
        :title="`Добавить полиграф`"
        :icon-class="`bi bi-heart-pulse fs-1`"
        @onclick="tabsData.tabAction = tabsData.tabAction ? '' : 'create';"
      />
      <IconRelative 
        v-show="tabsData.currentTab == 'InvestigateTab'"
        :title="`Добавить расследование`"
        :icon-class="`bi bi-incognito fs-1`"
        @onclick="tabsData.tabAction = tabsData.tabAction ? '' : 'create';"
      />
      <IconRelative 
        v-show="tabsData.currentTab == 'InquiryTab'"
        :title="`Добавить запрос`"
        :icon-class="`bi bi-question-square fs-1`"
        @onclick="tabsData.tabAction = tabsData.tabAction ? '' : 'create';"
      />
      <IconRelative
        :title="`Версия для печати`"
        :icon-class="`bi bi-printer fs-1`"
        @click="stateAnketa.share.printPage = !stateAnketa.share.printPage"
      />
    </div>
  </div>
  <nav
    v-if="!stateAnketa.share.printPage"
    class="nav nav-tabs nav-justified"
    role="tablist"
  >
    <button
      v-for="(tab, idx) in tabsData.tabs"
      :key="idx"
      class="nav-link"
      :class="{ active: idx === 0 }"
      :data-bs-target="`#${tab[0]}`"
      data-bs-toggle="tab"
      type="button"
      role="tab"
      @click="
        tabsData.currentTab = (tab[0] as string); 
        tabsData.tabAction = ''
      "
    >
      {{ tab[1] }}
    </button>
  </nav>
  <div :class="{ 'tab-content': !stateAnketa.share.printPage }" >
    <div
      class="py-3 show active"
      id="AnketaTab"
      :class="{ 'tab-pane fade mb-1': !stateAnketa.share.printPage }"
      role="tabpanel"
    >
      <AnketaTab/>
    </div>
    <div
      class="py-3"
      id="CheckTab"
      :class="{ 'tab-pane fade mb-1': !stateAnketa.share.printPage }"
      role="tabpanel"
    >
      <CheckTab
        :tab-action="tabsData.tabAction"
        :current-tab="tabsData.currentTab"
        @cancel="tabsData.tabAction = ''"
       />
    </div>
    <div
      class="py-3"
      id="RobotTab"
      :class="{ 'tab-pane fade mb-1': !stateAnketa.share.printPage }"
      role="tabpanel"
    >
      <RobotTab/>
    </div>
    <div
      class="py-3"
      id="PoligrafTab"
      :class="{ 'tab-pane fade mb-1': !stateAnketa.share.printPage }"
      role="tabpanel"
    >
      <PoligrafTab
        :tab-action="tabsData.tabAction"
        :current-tab="tabsData.currentTab"
        @cancel="tabsData.tabAction = ''"
       />
    </div>
    <div
      class="py-3"
      id="InvestigateTab"
      :class="{ 'tab-pane fade mb-1': !stateAnketa.share.printPage }"
      role="tabpanel"
    >
      <InvestigateTab
        :tab-action="tabsData.tabAction"
        :current-tab="tabsData.currentTab"
        @cancel="tabsData.tabAction = ''"
       />
    </div>
    <div
      class="py-3"
      id="InquiryTab"
      :class="{ 'tab-pane fade mb-1': !stateAnketa.share.printPage }"
      role="tabpanel"
    >
      <InquiryTab
        :tab-action="tabsData.tabAction"
        :current-tab="tabsData.currentTab"
        @cancel="tabsData.tabAction = ''"
       />
    </div>
    <div
      class="py-3"
      id="OneSTab"
      :class="{ 'tab-pane fade mb-1': !stateAnketa.share.printPage }"
      role="tabpanel"
    >
      <OneSTab/>
    </div>
  </div>
</template>
