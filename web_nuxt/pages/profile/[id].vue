<script setup lang="ts">
import type { Persons } from "@/types";
import type { TabsItem } from "@nuxt/ui";

await preloadComponents(["TabsAnketaTab", "TabsSharedTab", "TabsExplorerTab"]);

const route = useRoute();

const candId = computed(() => route.params.id) as Ref<string>;

provide("candId", candId);

const person = ref({} as Persons);
const region = ref("");

const { refresh, status } = await useLazyAsyncData("anketa", async () => {
  person.value = (await useFetchAuth(
    "/route/items/persons/" + candId.value
  )) as Persons;
});

provide("person", person);

const editState = computed(() => {
  return (
    person.value.editable &&
    stateUser.value.role == "user" &&
    stateUser.value.id == person.value.user_id
  );
});

async function switchSelf(): Promise<void> {
  if (person.value.user_id != stateUser.value.id) {
    if (person.value.editable) {
      if (
        !confirm(
          "Анкета редактируется другим пользователем. Переключить режим редактирования?"
        )
      ) {
        return;
      }
    }
    if (!confirm("Вы хотите назначить анкету на себя?")) {
      return;
    }
  } else if (!confirm("Переключить режим редактирования?")) {
    return;
  }
  status.value = "pending";
  person.value = (await useFetchAuth(
    "/route/anketa/self/" + candId.value
  )) as Persons;
  status.value = "success";
}

async function changeRegion(): Promise<void> {
  if (region.value == person.value.region) {
    return;
  }
  if (!confirm("Вы действительно хотите изменить регион?")) {
    region.value = person.value.region;
    return;
  }
  status.value = "pending";
  const { message } = (await useFetchAuth(
    `/route/anketa/region/${candId.value}`,
    {
      params: {
        region: region.value,
      },
    }
  )) as Record<string, string>;
  status.value = "success";
  emitMessage(message);
  if (message == "success") {
    navigateTo("/persons");
  } else {
    region.value = person.value.region;
  }
}

const items: TabsItem[] = [
  {
    slot: "anketa",
    label: "Анкета",
    icon: "i-heroicons-user",
  },
  {
    slot: "checks",
    label: "Проверки",
    icon: "i-heroicons-check-circle",
  },
  {
    slot: "poligrafs",
    label: "Полиграф",
    icon: "i-heroicons-bolt",
  },
  {
    slot: "investigations",
    label: "Расследования",
    icon: "i-heroicons-briefcase",
  },
  {
    slot: "inquiries",
    label: "Запросы",
    icon: "i-heroicons-document-text",
  },
  {
    slot: "explorer",
    label: "Файлы",
    icon: "i-heroicons-folder",
  },
] satisfies TabsItem[];
</script>

<template>
  <div class="mb-6">
    <div class="flex items-center justify-between mb-6">
      <USkeleton v-if="status == 'pending'" class="py-1 h-10 w-96" />
      <div v-else class="py-1">
        <h3 class="text-2xl text-red-800 font-bold">
          {{
            `${person.surname} ${person.firstname} ${person.patronymic ?? ""}`
          }}
        </h3>
      </div>
      <div v-if="stateUser.role == 'user'" class="flex items-center space-x-4">
        <UTooltip text="Изменить регион">
          <USelect
            id="region"
            v-model="region"
            icon="i-heroicons-map"
            :items="[
              'Главный офис',
              'РЦ Юг',
              'РЦ Запад',
              'РЦ Урал',
              'РЦ Восток',
            ]"
            :placeholder="person.region"
            :disabled="
              (person.region != stateUser.region &&
                stateUser.region != 'Главный офис') ||
              !editState
            "
            @change="changeRegion"
          />
        </UTooltip>
        <UTooltip text="Переключить режим">
          <UButton
            :loading="status === 'pending'"
            :disabled="person.region != stateUser.region"
            :color="
              !person.editable
                ? 'secondary'
                : person.user_id == stateUser.id
                ? 'success'
                : 'error'
            "
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
    <UTabs
      :unmount-on-hide="false"
      color="secondary"
      :items="items"
      variant="link"
      class="gap-4 w-full"
      :ui="{ trigger: 'flex-1' }"
    >
      <template #anketa>
        <TabsAnketaTab @update="refresh()" />
      </template>
      <template #checks="{ item }">
        <TabsSharedTab :view="item.slot" />
      </template>
      <template #poligrafs="{ item }">
        <TabsSharedTab :view="item.slot" />
      </template>
      <template #investigations="{ item }">
        <TabsSharedTab :view="item.slot" />
      </template>
      <template #inquiries="{ item }">
        <TabsSharedTab :view="item.slot" />
      </template>
      <template #explorer>
        <TabsExplorerTab />
      </template>
    </UTabs>
  </div>
</template>
