<script setup lang="ts">
import { onBeforeMount } from "vue";
import { server, stateAnketa, stateClassify, stateUser } from "@/state/state";
import { useFetchAuth } from "@/utils/auth";

const AnketaTab = resolveComponent("TabsAnketaTab");
const CheckTab = resolveComponent("TabsCheckTab");
const PoligrafTab = resolveComponent("TabsPoligrafTab");
const InvestigateTab = resolveComponent("TabsInvestigateTab");
const InquiryTab = resolveComponent("TabsInquiryTab");

const route = useRoute();

const anketaState = stateAnketa();
const classifyState = stateClassify();
const userState = stateUser();

onBeforeMount(async () => {
  anketaState.share.value.candId = route.params.id as string;
  try {
    const authFetch = useFetchAuth();
    const data = await authFetch(
      `${server}/profile/${anketaState.share.value.candId}`
    );
    const resp = data as any;
    const anketaKeys = Object.keys(anketaState.anketa.value);
    for (let i = 0; i < anketaKeys.length; i++) {
      anketaState.anketa.value[
        anketaKeys[i] as keyof typeof anketaState.anketa.value
      ] = resp[i];
    }
    anketaState.getImage();
  } catch (error: unknown) {
    console.error(error);
  }
});

async function switchStandings() {
  anketaState.getItem("persons", "self");
}

const tabs = [{
  slot: 'anketaTab',
  label: 'Анкета',
  component: AnketaTab
}, {
  slot: 'checkTab',
  label: 'Проверки',
  component: CheckTab
}, {
  slot: 'poligrafTab',
  label: 'Полиграф',
  component: PoligrafTab
}, {
  slot: 'investigateTab',
  label: 'Расследования',
  component: InvestigateTab
}, {
  slot: 'inquiryTab',
  label: 'Запросы',
  component: InquiryTab
}]
</script>

<template>
  <LayoutsMenu>
    <DivsPhotoCard />
    <div class="py-8">
      <h3 class="text-2xl text-red-800 font-bold">
        {{
          `${anketaState.anketa.value.persons.surname} ${
            anketaState.anketa.value.persons.firstname
          } ${
            anketaState.anketa.value.persons.patronymic
              ? " " + anketaState.anketa.value.persons.patronymic
              : ""
          }`
        }}
      </h3>
    </div>
    <div 
      v-if="
        userState.user.value.role == classifyState.classes.value.roles['user']
      "
      class="absolute object-right"
    >
      <UButton
        :title="
          anketaState.anketa.value.persons['standing']
            ? 'Отключить режим проверки'
            : 'Включить режим проверки'
        "
        variant="link"
        :icon="
          anketaState.anketa.value.persons['standing']
            ? 'i-heroicons-x'
            : 'i-heroicons-suitcase'
        "
        @click="switchStandings"
      />
    </div>
    <UTabs :items="tabs" class="w-full">
      <template v-for="item, idx in tabs" #[item.slot] :key="idx">
        <component :is="item['component']" />
      </template>
    </UTabs>
  </LayoutsMenu>
</template>
