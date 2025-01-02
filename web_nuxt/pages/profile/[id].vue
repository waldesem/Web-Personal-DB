<script setup lang="ts">
import type { Persons } from "@/types";

await preloadComponents([
  "TabsAnketaTab",
  "TabsCheckTab",
  "TabsPoligrafTab",
  "TabsInvestigateTab",
  "TabsInquiryTab",
]);

const authFetch = useFetchAuth();

const toast = useToast();
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

const editState = computed(() => {
  return (
    person.value["editable"] &&
    stateUser.value.role == "user" &&
    stateUser.value.id == person.value["user_id"]
  );
});

provide("editable", editState);

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
  }
  emitMessage(message);
}

async function changeRegion(): Promise<void> {
  if (confirm("Вы действительно хотите изменить регион?")) {
    pending.value = true;
    const { message } = (await authFetch(
      `/route/anketa/region/${candId.value}`,
      {
        params: {
          region: region.value,
        },
      }
    )) as Record<string, string>;
    pending.value = false;
    emitMessage(message);
    if (message == "success") {
      person.value.region = region.value;
    }
  } else {
    region.value = person.value.region;
  }
}

function emitMessage(message: string) {
  if (message == "success") {
    toast.add({
      icon: "i-heroicons-information-circle",
      title: "Информация",
      description: "Информация обновлена",
      color: "primary",
    });
  } else {
    toast.add({
      icon: "i-heroicons-exclamation-triangle",
      title: "Внимание",
      description: "Ошибка обновления информации",
      color: "red",
    });
  }
}
</script>

<template>
  <div class="mb-6">
    <div class="flex items-center justify-between mb-3">
      <div class="flex items-center space-x-4">
        <USkeleton v-if="!person" class="my-6 h-8 w-1/3" />
        <div v-else class="py-1">
          <h3 class="text-2xl text-red-800 font-bold">
            {{ `${person['surname']} ${person['firstname']} ${
              person['patronymic'] ? person['patronymic'] : ''
            }` }}
          </h3>
        </div>
        <USelect
          v-model="region"
          :options="[
            'Главный офис',
            'РЦ Юг',
            'РЦ Запад',
            'РЦ Урал',
            'РЦ Восток',
          ]"
          :disabled="!person.editable"
          :placeholder="person['region'] || 'Регион'"
          @change="changeRegion"
        />
      </div>
      <UButton
        :loading="pending || status === 'pending'"
        :color="
          !person.editable
            ? 'blue'
            : person.user_id != stateUser.id
            ? 'red'
            : 'green'
        "
        size="sm"
        @click="switchSelf"
      >
        {{
          !person.editable
            ? "Анкета доступна для редактирования"
            : person.user_id != stateUser.id
            ? "Анкета редактируется другим пользователем"
            : "Анкета редактируется текущим пользователем"
        }}
      </UButton>
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
    </UTabs>
  </div>
</template>
