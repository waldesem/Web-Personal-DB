<script setup lang="ts">
import { server, stateAnketa, stateClassify, stateUser } from "@/state/state";
import { useFetchAuth } from "@/utils/auth";
import type { Profile } from "@/utils/interfaces";

const anketaState = stateAnketa();
const classifyState = stateClassify();
const userState = stateUser();
const route = useRoute();

anketaState.share.value.candId = route.params.id as string;
try {
  const authFetch = useFetchAuth();
  anketaState.anketa.value = (await authFetch(
    `${server}/profile/${anketaState.share.value.candId}`
  )) as Profile;
  await anketaState.getImage();
} catch (error: unknown) {
  console.error(error);
}

const tabs = [
  {
    slot: "anketaTab",
    label: "Анкета",
  },
  {
    slot: "checkTab",
    label: "Проверки",
  },
  {
    slot: "poligrafTab",
    label: "Полиграф",
  },
  {
    slot: "investigateTab",
    label: "Расследования",
  },
  {
    slot: "inquiryTab",
    label: "Запросы",
  },
];

async function switchStandings() {
  anketaState.getItem("persons", "self");
}
</script>

<template>
  <LayoutsMenu>
    <DivsPhotoCard />
    <div
      v-if="
        userState.user.value.role == classifyState.classes.value.roles['user']
      "
      class="relative"
    >
      <div class="absolute top-0 right-0" title="Загрузить json">
        <UButton
          :title="
            anketaState.anketa.value.persons['standing']
              ? 'Отключить режим проверки'
              : 'Включить режим проверки'
          "
          variant="link"
          size="xl"
          :color="anketaState.anketa.value.persons['standing'] ? 'red' : 'green'"
          :icon="
            anketaState.anketa.value.persons['standing']
              ? 'i-heroicons-bolt'
              : 'i-heroicons-bolt-slash'
          "
          @click="switchStandings"
        />
      </div>
    </div>  
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
    <UTabs :items="tabs" class="w-full">
      <template #anketaTab><TabsAnketaTab /></template>
      <template #checkTab><TabsCheckTab /></template>
      <template #poligrafTab><TabsPoligrafTab /></template>
      <template #investigateTab><TabsInvestigateTab /></template>
      <template #inquiryTab><TabsInquiryTab /></template>
    </UTabs>
  </LayoutsMenu>
</template>
