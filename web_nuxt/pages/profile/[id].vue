<script setup lang="ts">
import { usePersonState } from "@/composables/personState";
import type { TabsItem } from "@nuxt/ui";
import type { Persons } from "@/types";

await preloadComponents(["ItemsAnketaTab", "ItemsSharedTab"]);

const route = useRoute();
const userState = useUserState();
const personState = usePersonState();

const candId = computed(() => route.params.id as string);
provide("candId", candId);

// const person = ref({} as Persons);
const region = ref("");

const { status, refresh } = await useLazyAsyncData("persons", async () => {
  personState.person.value = (await fetchAuth(
    "/route/items/persons/" + candId.value
  )) as Persons;
});
provide("status", status);

const editable = computed(() => {
  return (
    personState.person.value.editable &&
    userState.value.role == "user" &&
    userState.value.id == personState.person.value.user_id
  );
});
provide("editable", editable);

async function switchSelf(): Promise<void> {
  if (personState.person.value.user_id != userState.value.id) {
    if (personState.person.value.editable) {
      if (
        !confirm(
          "Анкета редактируется другим пользователем. Переключить режим?"
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
  personState.person.value = (await fetchAuth(
    "/route/anketa/self/" + personState.person.value.id
  )) as Persons;
  status.value = "success";
}

async function changeRegion() {
  if (region.value == personState.person.value.region) {
    return;
  }
  if (!confirm("Вы действительно хотите изменить регион?")) {
    region.value = personState.person.value.region;
    return;
  }
  status.value = "pending";
  const { message } = (await fetchAuth(
    `/route/anketa/region/${personState.person.value.id}`,
    {
      params: {
        region: region.value,
      },
    }
  )) as Record<string, string>;
  if (message == "success") {
    makeToast(message, "Регион успешно обновлен");
    return navigateTo("/persons");
  } else {
    makeToast();
    region.value = personState.person.value.region;
    status.value = "error";
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
] satisfies TabsItem[];
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <USkeleton v-if="status == 'pending'" class="py-1 h-10 w-96" />
      <div v-else class="py-1">
        <h3 class="text-2xl text-red-800 font-bold">
          {{
            `${personState.person.value.surname} ${
              personState.person.value.firstname
            } ${personState.person.value.patronymic ?? ""}`
          }}
        </h3>
      </div>
      <div v-if="userState.role == 'user'" class="flex items-center space-x-4">
        <UTooltip text="Изменить регион">
          <USelect
            id="region"
            v-model="region"
            :items="[
              'Главный офис',
              'РЦ Юг',
              'РЦ Запад',
              'РЦ Урал',
              'РЦ Восток',
            ]"
            :placeholder="personState.person.value.region"
            :disabled="
              (personState.person.value.region != userState.region &&
                userState.region != 'Главный офис') ||
              !editable
            "
            @change="changeRegion"
          />
        </UTooltip>
        <UButton
          :loading="status === 'pending'"
          :disabled="personState.person.value.region != userState.region"
          :color="
            !personState.person.value.editable
              ? 'secondary'
              : personState.person.value.user_id == userState.id
              ? 'success'
              : 'error'
          "
          @click="switchSelf"
        >
          {{
            !personState.person.value.editable
              ? "Анкета доступна для редактирования"
              : personState.person.value.user_id == userState.id
              ? "Анкета назначена текущему пользователю"
              : "Анкета редактируется другим пользователем"
          }}
        </UButton>
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
        <ItemsAnketaTab
          :person="personState.person.value"
          :rows="12"
          @refresh="refresh"
        />
      </template>
      <template #checks="{ item }">
        <ItemsSharedTab :view="item.slot" :rows="16" />
      </template>
      <template #poligrafs="{ item }">
        <ItemsSharedTab :view="item.slot" :rows="4" />
      </template>
      <template #investigations="{ item }">
        <ItemsSharedTab :view="item.slot" :rows="3" />
      </template>
      <template #inquiries="{ item }">
        <ItemsSharedTab :view="item.slot" :rows="3" />
      </template>
    </UTabs>
  </div>
</template>
