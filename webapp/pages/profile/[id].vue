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

// const items = [{
//   slot: 'anketaTab',
//   label: 'Anketa',
//   component: AnketaTab
// }, {
//   slot: 'checkTab',
//   label: 'Check',
//   component: CheckTab
// }, {
//   slot: 'poligrafTab',
//   label: 'Poligraf',
//   component: PoligrafTab
// }, {
//   slot: 'investigateTab',
//   label: 'Investigate',
//   component: InvestigateTab
// }, {
//   slot: 'inquiryTab',
//   label: 'Inquiry',
//   component: InquiryTab
// }]

async function switchStandings() {
  anketaState.getItem("persons", "self");
}
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
    <!-- <UTabs :items="items" class="w-full">
      <template v-for="item, idx in items" #[item.slot] :key="idx">
        <component :is="item['component']" />
      </template>
    </UTabs> -->
  </LayoutsMenu>
</template>
