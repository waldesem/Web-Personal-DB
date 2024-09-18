<script setup lang="ts">
import { server, stateUser } from "@/state/state";
import { useFetchAuth } from "@/utils/auth";

const authFetch = useFetchAuth();
const userState = stateUser();
const route = useRoute();

const candId = computed(() => route.params.id) as unknown as string;

const { data, refresh } = await useAsyncData("anketa", async () => {
  await getItem("persons");
});

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
  },
};

const badge = computed(() => {
  if (anketaState.anketa.value.persons["editable"]) {
    if (
      anketaState.anketa.value.persons["user_id"] == userState.value.id
    ) {
      return badgeItems.current;
    } else if (
      anketaState.anketa.value.persons["user_id"] != userState.value.id
    ) {
      return badgeItems.thirdparty;
    }
  }
  return badgeItems.others;
});

const editState = computed(() => {
  return (
    anketaState.anketa.value.persons["editable"] &&
    userState.value.role == classifyState.classes.value.roles["user"] &&
    userState.value.id == anketaState.anketa.value.persons["user_id"]
  );
});

provide("editState", editState);

async function switchSelf(): Promise<void> {
  if (!confirm("Вы действительно хотите включить/выключить режим правки")) {
    return;
  }
  const response = await authFetch(
    `${server}/self/${anketaState.share.value.candId}`
  );
  console.log(response);
  refresh();
}
</script>

<template>
  <LayoutsMenu>
    <DivsPhotoCard />
    <div
      v-if="
        userState.role == classifyState.classes.value.roles['user']
      "
      class="relative"
    >
      <div class="absolute bottom-0 right-20">
        <UButton variant="link" size="xl" @click="switchSelf">
          <div class="animate-pulse" style="width: 30px">
            <UBadge :color="(badge.color as any)" variant="solid">
              {{ badge.label }}
            </UBadge>
          </div>
        </UButton>
      </div>
      <div class="absolute top-0 right-10">
        <UButton variant="link" size="xl" to="/profile/print">
          <UIcon name="i-heroicons-printer" class="w-8 h-8" />
        </UButton>
      </div>
    </div>
    <ElementsHeaderDiv
      :div="'py-3'"
      :header="`${anketaState.anketa.value.persons.surname} ${
        anketaState.anketa.value.persons.firstname
      } ${
        anketaState.anketa.value.persons.patronymic
          ? anketaState.anketa.value.persons.patronymic
          : ''
      }`"
    />
    <UTabs :items="tabs">
      <template #anketaTab><TabsAnketaTab :candId="candId" :person="person" /></template>
      <template #checkTab><TabsCheckTab :candId="candId" /></template>
      <template #poligrafTab><TabsPoligrafTab :candId="candId" /></template>
      <template #investigateTab><TabsInvestigateTab :candId="candId" /></template>
      <template #inquiryTab><TabsInquiryTab :candId="candId" /></template>
    </UTabs>
  </LayoutsMenu>
</template>
