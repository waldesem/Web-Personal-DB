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
    icon: "i-heroicons-user",
  },
  {
    slot: "checkTab",
    label: "Проверки",
    icon: "i-heroicons-check-circle",
  },
  {
    slot: "poligrafTab",
    label: "Полиграф",
    icon: "i-heroicons-bolt",
  },
  {
    slot: "investigateTab",
    label: "Расследования",
    icon: "i-heroicons-briefcase",
  },
  {
    slot: "inquiryTab",
    label: "Запросы",
    icon: "i-heroicons-document-text",
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
  if (anketaState.anketa.value.persons['editable']) {
    if (anketaState.anketa.value.persons['user_id'] == userState.user.value.userId) {
      return badgeItems.current
    } else if (anketaState.anketa.value.persons['user_id'] != userState.user.value.userId) {
      return badgeItems.thirdparty
    }
  }
  return badgeItems.others
})

const editState = computed(() => {
  return anketaState.anketa.value.persons['editable'] && userState.user.value.role == classifyState.classes.value.roles['user'] && userState.user.value.userId == anketaState.anketa.value.persons['user_id']
})

provide("editState", editState)
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
      <div class="absolute top-0 right-20">
        <UButton
          variant="link"
          size="xl"
          :color="
            anketaState.anketa.value.persons['editable'] ? 'red' : 'green'
          "
          @click="anketaState.getItem('persons', 'self')"
        >
          <div class="animate-pulse" style="width: 30px;">
            <UBadge
              :color="badge.color" 
              variant="solid"

            >
              {{ badge.label }}
            </UBadge>
          </div>
        </UButton>
      </div>
      <div class="absolute bottom-10 right-10">
        <UButton
          variant="link"
          size="xl"
          to="/profile/print"
        >
          <UIcon name="i-heroicons-printer" class="w-8 h-8" />
        </UButton>
      </div>
    </div>
    <ElementsHeaderDiv 
      :header="
        anketaState.anketa.value.persons.surname + ' ' +
        anketaState.anketa.value.persons.firstname + ' ' +
        anketaState.anketa.value.persons.patronymic
          ? anketaState.anketa.value.persons.patronymic : ''
        "
    />
    <UTabs :items="tabs" class="w-full">
      <template #anketaTab><TabsAnketaTab /></template>
      <template #checkTab><TabsCheckTab /></template>
      <template #poligrafTab><TabsPoligrafTab /></template>
      <template #investigateTab><TabsInvestigateTab /></template>
      <template #inquiryTab><TabsInquiryTab /></template>
    </UTabs>
  </LayoutsMenu>
</template>
