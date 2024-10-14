<script setup lang="ts">
import type { Persons } from "@/types/interfaces";

const authFetch = useFetchAuth();
const userState = useUserState();

const route = useRoute();

const candId = computed(() => route.params.id) as Ref<string>;

const person = ref({} as Persons);

const { refresh } = await useAsyncData("anketa", async () => {
  const response = await authFetch("/api/persons/" + candId.value);
  person.value = response as Persons;
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
  if (person.value["editable"]) {
    if (person.value["user_id"] == userState.value.id) {
      return badgeItems.current;
    } else if (person.value["user_id"] != userState.value.id) {
      return badgeItems.thirdparty;
    }
  }
  return badgeItems.others;
});

const editState = computed(() => {
  return (
    person.value["editable"] &&
    userState.value.role == "user" &&
    userState.value.id == person.value["user_id"]
  );
});

async function switchSelf(): Promise<void> {
  if (!confirm("Вы действительно хотите включить/выключить режим правки")) {
    return;
  }
  await authFetch("/api/self/" + candId.value);
  await refresh();
}

onBeforeRouteLeave((to, from, next) => {
  clearNuxtData();
  next();
});
</script>

<template>
  <div>
    <DivsPhotoCard
      :cand-id="candId"
      :destination="person['destination']"
      :editable="editState"
    />
    <div v-if="userState.role == 'user'" class="relative">
      <div class="absolute bottom-0 right-20">
        <UButton variant="link" size="xl" @click="switchSelf">
          <div class="animate-pulse" style="width: 30px">
            <UBadge :color="(badge.color as any)" variant="solid">
              {{ badge.label }}
            </UBadge>
          </div>
        </UButton>
      </div>
    </div>
    <ElementsHeaderDiv
      :div="'py-3'"
      :header="`${person['surname']} ${person['firstname']} ${
        person['patronymic'] ? person['patronymic'] : ''
      }`"
    />
    <UTabs :items="tabs">
      <template #anketaTab
        ><TabsAnketaTab
          :cand-id="candId"
          :editable="editState"
          :person="person"
          @update="refresh()"
      /></template>
      <template #checkTab
        ><TabsCheckTab :cand-id="candId" :editable="editState"
      /></template>
      <template #poligrafTab
        ><TabsPoligrafTab :cand-id="candId" :editable="editState"
      /></template>
      <template #investigateTab
        ><TabsInvestigateTab :cand-id="candId" :editable="editState"
      /></template>
      <template #inquiryTab
        ><TabsInquiryTab :cand-id="candId" :editable="editState"
      /></template>
    </UTabs>
  </div>
</template>
