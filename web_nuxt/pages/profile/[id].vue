<script setup lang="ts">
import { useFileDialog } from "@vueuse/core";
import type { TabsItem } from "@nuxt/ui";
import type { Persons, Regions } from "@/types";

await preloadComponents(["ContentAnketaTab", "ContentSharedView"]);

const route = useRoute();
const userState = useUserState();

const candId = computed(() => route.params.id as string);
provide("candId", candId);

const person = ref({} as Persons);
const region = ref("" as Regions);

const { status, refresh } = await useLazyAsyncData("persons", async () => {
  person.value = (await fetchAuth(
    "/route/items/persons/" + candId.value
  )) as Persons;
});
provide("status", status);

const editable = computed(() => {
  return (
    person.value.editable &&
    userState.value.role == "user" &&
    userState.value.id == person.value.user_id
  );
});
provide("editable", editable);

async function switchSelf(): Promise<void> {
  if (person.value.user_id != userState.value.id) {
    if (person.value.editable) {
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
  person.value = (await fetchAuth(
    "/route/anketa/self/" + person.value.id
  )) as Persons;
  status.value = "success";
}

async function changeRegion() {
  if (region.value == person.value.region) {
    return;
  }
  if (!confirm("Вы действительно хотите изменить регион?")) {
    region.value = person.value.region;
    return;
  }
  status.value = "pending";
  const { message } = (await fetchAuth(
    `/route/anketa/region/${person.value.id}`,
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
    region.value = person.value.region;
    status.value = "error";
  }
}

const { open, reset, onCancel, onChange } = useFileDialog();

onChange(async (files) => {
  if (!files) return;
  const formData = new FormData();
  for (const file of files) {
    const maxSize = 10 * 1024 * 1024;
    if (file.size > maxSize) {
      makeToast("info", "Размер одного файла не должен превышать 10 МБ");
      continue;
    }
    formData.append("file", file);
  }
  const { message } = (await fetchAuth(`/route/anketa/files/${candId.value}`, {
    method: "POST",
    body: formData,
  })) as Record<string, string>;
  if (message == "success") {
    makeToast("success", "Файлы успешно загружены");
  } else {
    makeToast();
  }
  reset();
});

onCancel(() => {
  reset();
});

const items: TabsItem[] = [
  {
    slot: "anketa" as const,
    label: "Анкета",
    icon: "i-heroicons-user",
  },
  {
    slot: "checks" as const,
    label: "Проверки",
    icon: "i-heroicons-check-circle",
  },
  {
    slot: "poligrafs" as const,
    label: "Полиграф",
    icon: "i-heroicons-bolt",
  },
  {
    slot: "investigations" as const,
    label: "Расследования",
    icon: "i-heroicons-briefcase",
  },
  {
    slot: "inquiries" as const,
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
            `${person.surname} ${person.firstname} ${person.patronymic ?? ""}`
          }}
        </h3>
      </div>
      <div v-if="userState.role == 'user'" class="flex items-center space-x-4">
        <UButton
          :loading="status === 'pending'"
          variant="outline"
          icon="i-heroicons-cloud-arrow-up"
          label="Загрузить файлы"
          @click="open()"
        />
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
            :placeholder="person.region"
            :disabled="
              (person.region != userState.region &&
                userState.region != 'Главный офис') ||
              !editable
            "
            @change="changeRegion"
          />
        </UTooltip>
        <UButton
          :loading="status === 'pending'"
          :disabled="person.region != userState.region"
          :color="
            !person.editable
              ? 'secondary'
              : person.user_id == userState.id
              ? 'success'
              : 'error'
          "
          :label="
            !person.editable
              ? 'Доступно  для редактирования'
              : person.user_id == userState.id
              ? 'Назначено текущему пользователю'
              : 'Редактируется другим пользователем'
          "
          @click="switchSelf"
        />
      </div>
    </div>
    <UTabs
      :unmount-on-hide="false"
      color="info"
      :items="items"
      variant="pill"
      class="gap-4 w-full"
      :ui="{ trigger: 'flex-1' }"
    >
      <template #anketa>
        <ContentAnketaTab :person="person" :rows="12" @refresh="refresh" />
      </template>
      <template #checks="{ item }">
        <ContentSharedView :view="item.slot" :rows="16" />
      </template>
      <template #poligrafs="{ item }">
        <ContentSharedView :view="item.slot" :rows="4" />
      </template>
      <template #investigations="{ item }">
        <ContentSharedView :view="item.slot" :rows="3" />
      </template>
      <template #inquiries="{ item }">
        <ContentSharedView :view="item.slot" :rows="3" />
      </template>
    </UTabs>
  </div>
</template>
