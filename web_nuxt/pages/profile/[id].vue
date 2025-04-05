<script setup lang="ts">
import type { Persons } from "@/types";

await preloadComponents([
  "TabsAnketaTab",
  "TabsCheckTab",
  "TabsPoligrafTab",
  "TabsInvestigateTab",
  "TabsInquiryTab",
  "TabsExplorerTab",
]);
await prefetchComponents([
  "ElementsCardDiv",
  "ElementsDivMenu",
  "ElementsTabMenu",
]);

const authFetch = useFetchAuth();

const route = useRoute();

const candId = computed(() => route.params.id) as Ref<string>;

provide("candId", candId);

const person = ref({} as Persons);
const pending = ref(false);
const region = ref("");

const { refresh, status } = await useLazyAsyncData("anketa", async () => {
  person.value = (await authFetch(
    "/route/items/persons/" + candId.value
  )) as Persons;
});

provide("person", person);
provide("status", status);

const editState = computed(() => {
  return (
    person.value.editable &&
    stateUser.value.role == "user" &&
    stateUser.value.id == person.value.user_id
  );
});

provide("editable", editState);

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
  {
    slot: "explorerTab",
    label: "Файлы",
    icon: "i-heroicons-folder",
  },
];

async function switchSelf(): Promise<void> {
  if (person.value.user_id != stateUser.value.id) {
    if (!confirm("Вы хотите назначить анкету на себя?")) {
      return;
    }
  } else if (!confirm("Переключить режим редактирования?")) {
    return;
  }
  pending.value = true;
  const { message } = (await authFetch(
    "/route/anketa/self/" + candId.value
  )) as Record<string, string>;
  pending.value = false;
  if (message == "success") {
    person.value.editable = !person.value.editable;
    person.value.user_id = stateUser.value.id;
  } else {
    emitMessage(message);
  }
}

async function changeRegion(): Promise<void> {
  if (region.value == person.value.region) {
    return;
  }
  if (!confirm("Вы действительно хотите изменить регион?")) {
    region.value = person.value.region;
    return;
  }
  pending.value = true;
  const { message } = (await authFetch(`/route/anketa/region/${candId.value}`, {
    params: {
      region: region.value,
    },
  })) as Record<string, string>;
  pending.value = false;
  emitMessage(message);
  if (message == "success") {
    navigateTo("/persons");
  } else {
    region.value = person.value.region;
  }
}
</script>

<template>
  <div class="mb-6">
    <div class="flex items-center justify-between mb-6">
      <USkeleton v-if="status == 'pending'" class="py-1 h-10 w-96" />
      <div v-else class="py-1">
        <h3 class="text-2xl text-red-800 font-bold">
          {{
            `${person.surname} ${person.firstname} ${
              person.patronymic ? person.patronymic : ""
            }`
          }}
        </h3>
      </div>
      <div v-if="stateUser.role == 'user'" class="flex items-center space-x-4">
        <UTooltip text="Изменить регион">
          <USelect
            id="region"
            v-model="region"
            icon="i-heroicons-map"
            color="primary"
            :options="[
              'Главный офис',
              'РЦ Юг',
              'РЦ Запад',
              'РЦ Урал',
              'РЦ Восток',
            ]"
            :placeholder="person.region"
            :disabled="
              person.region != stateUser.region &&
              stateUser.region != 'Главный офис'
            "
            @change="changeRegion"
          />
        </UTooltip>
        <UTooltip text="Переключить режим редактирования">
          <UButton
            :loading="pending || status === 'pending'"
            :disabled="person.region != stateUser.region"
            :color="
              !person.editable
                ? 'blue'
                : person.user_id == stateUser.id
                ? 'green'
                : 'red'
            "
            size="sm"
            @click="switchSelf"
          >
            {{
              !person.editable
                ? "Анкета доступна для редактирования"
                : person.user_id == stateUser.id
                ? "Анкета назначена текущему пользователю"
                : "Анкета редактируется другим пользователем"
            }}
          </UButton>
        </UTooltip>
      </div>
    </div>
    <UTabs :items="tabs">
      <template #anketaTab>
        <TabsAnketaTab @update="refresh()" />
      </template>
      <template #checkTab>
        <TabsCheckTab />
      </template>
      <template #poligrafTab>
        <TabsPoligrafTab />
      </template>
      <template #investigateTab>
        <TabsInvestigateTab />
      </template>
      <template #inquiryTab>
        <TabsInquiryTab />
      </template>
      <template #explorerTab>
        <TabsExplorerTab />
      </template>
    </UTabs>
  </div>
</template>
