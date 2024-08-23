<script setup lang="ts">
import { server, stateAnketa, stateClassify, stateUser } from "@/state/state";
import { useFetchAuth } from "@/utils/auth";
import type { Profile } from "@/utils/interfaces";

const anketaState = stateAnketa();
const classifyState = stateClassify();
const userState = stateUser();
const route = useRoute();

anketaState.share.value.candId = route.params.id as string;

const authFetch = useFetchAuth();
anketaState.anketa.value = (await authFetch(
  `${server}/profile/${anketaState.share.value.candId}`
)) as Profile;
await anketaState.getImage();

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

const badgeItems = {
  current: {
    label: "Анкета редактируется текущим пользователем",
    color: "green",
  },
  thirdparty: {
    label: "Анкета редактируется другим пользователем",
    color: "red",
  },
  others: {
    label: "Анкета не редактируется пользователями",
    color: "blue",
  }
}

const badge = computed(() => {
  if (!anketaState.anketa.value.persons['editable']) {
    if (anketaState.anketa.value.persons['user_id'] == userState.user.value.userId) {
      return badgeItems.current
    } else if (anketaState.anketa.value.persons['user_id'] != userState.user.value.userId) {
      return badgeItems.thirdparty
    }
  }
  return badgeItems.others
})
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
      <div class="absolute top-0 right-0">
        <UButton
          variant="link"
          size="xl"
          :color="
            anketaState.anketa.value.persons['editable'] ? 'red' : 'green'
          "
          @click="anketaState.getItem('persons', 'self')"
        >
          <div class="animate-ping">
            <UBadge :color="badge.color" variant="subtle">{{ badge.label }}</UBadge>
          </div>
        </UButton>
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
