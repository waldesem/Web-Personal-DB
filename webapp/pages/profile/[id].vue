<script setup lang="ts">
import { onBeforeMount, ref } from "vue";
import { server, stateAnketa, stateClassify, stateUser } from "@/state/state";
import { axiosAuth } from "@/utils/auth";

const AnketaTab = resolveComponent('TabsAnketaTab');
const CheckTab = resolveComponent('TabsCheckTab');
const PoligrafTab = resolveComponent('TabsPoligrafTab');
const InvestigateTab = resolveComponent('TabsInvestigateTab');
const InquiryTab = resolveComponent('TabsInquiryTab');

const route = useRoute();

const anketaState = stateAnketa();
const classifyState = stateClassify();
const userState = stateUser();

onBeforeMount(async () => {
  anketaState.share.value.candId = route.params.id as string;
  try {
    const response = await axiosAuth.get(
      `${server}/profile/${anketaState.share.value.candId}`
    );
    const resp = response.data;
    const anketaKeys = Object.keys(anketaState.anketa.value);
    for (let i = 0; i < anketaKeys.length; i++) {
      anketaState.anketa.value[anketaKeys[i] as keyof typeof anketaState.anketa.value] =
        resp[i];
    }
    anketaState.getImage();
  } catch (error: any) {
    console.error(error);
  }
});

const currentTab = ref("anketaTab");

const tabsData = {
  anketaTab: ["Взять анкету", "Анкета", AnketaTab],
  checkTab: ["Добавить проверку", "Проверки", CheckTab, "bi-person-check"],
  poligrafTab: [
    "Добавить полиграф",
    "Полиграф",
    PoligrafTab,
    "bi-heart-pulse",
  ],
  investigateTab: [
    "Добавить расследования",
    "Расследования",
    InvestigateTab,
    "bi-incognito",
  ],
  inquiryTab: [
    "Добавить запрос",
    "Запросы",
    InquiryTab,
    "bi-journal-check",
  ],
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
  anketaState.getItem("persons", "self");
}

async function switchTabs(tab: string) {
  await closeCollapses();
  currentTab.value = tab;
}
</script>

<template>
  <LayoutsMenu>
    <DivsPhotoCard />
    <div class="row mb-3">
      <div class="col-md-10">
        <ElementsHeaderDiv
          :cls="'text-danger py-3'"
          :page-header="`${anketaState.anketa.value.persons.surname} ${
            anketaState.anketa.value.persons.firstname
          } ${
            anketaState.anketa.value.persons.patronymic
              ? ' ' + anketaState.anketa.value.persons.patronymic
              : ''
          }`"
        />
      </div>
      <div
        v-if="
          userState.user.value.role == classifyState.classes.value.roles['user']
        "
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
              anketaState.anketa.value.persons['user_id'] ==
                userState.user.value.userId &&
              anketaState.anketa.value.persons['standing']
            "
            :title="(tabsData[currentTab as keyof typeof tabsData][0] as string)"
            class="text-danger fs-1"
            style="cursor: pointer"
            data-bs-toggle="collapse"
            :href="'#clps_' + item.split('T')[0]"
          >
            <i
              class="bi"
              :class="tabsData[currentTab as keyof typeof tabsData][3]"
            ></i>
          </div>
        </div>
        <div v-if="currentTab == 'anketaTab'" class="position-relative">
          <button
            type="button"
            :class="
              anketaState.anketa.value.persons['standing']
                ? 'btn btn-link'
                : 'btn btn-outline-danger'
            "
            :title="
              anketaState.anketa.value.persons['standing']
                ? 'Отключить режим проверки'
                : 'Включить режим проверки'
            "
            @click="switchStandings"
          >
            <span
              v-if="anketaState.anketa.value.persons['standing']"
              class="spinner-grow text-danger"
              role="status"
            >
            </span>
            <div class="text-danger fs-5" v-else>
              <i class="bi bi-pencil-square"></i>
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
  </LayoutsMenu>
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
