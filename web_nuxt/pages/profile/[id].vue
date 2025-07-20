<script setup lang="ts">
import { useFileDialog } from "@vueuse/core";
import type { TabsItem } from "@nuxt/ui";
import type { Persons, PillsItems } from "@/types";

await preloadComponents(["ContentAnketaTab", "ContentSharedView"]);

const { $customFetch } = useNuxtApp();

const route = useRoute();
const userState = useUserState();

const candId = computed(() => route.params.id as string);
provide("candId", candId);

const {
  data: person,
  status,
  refresh,
} = await useCustomFetch<Persons>("/route/items/persons/" + candId.value, {
  server: false,
});
provide("status", status);

const editable = computed(() => {
  return (
    person.value &&
    person.value.editable &&
    userState.value.role == "user" &&
    userState.value.id == person.value.user_id
  );
});
provide("editable", editable);

async function switchSelf(): Promise<void> {
  if (person.value && person.value.user_id != userState.value.id) {
    if (person.value.editable) {
      if (
        !confirm(
          "Анкета редактируется другим пользователем. Переключить режим?"
        )
      ) {
        return;
      }
    } else if (!confirm("Вы хотите назначить анкету на себя?")) {
      return;
    }
  } else if (!confirm("Переключить режим редактирования?")) {
    return;
  }
  status.value = "pending";
  const { message } = (await $customFetch(
    "/route/anketa/self/" + person.value?.id
  )) as Record<string, string>;
  status.value = message as "success" | "error";
  if (message == "success") {
    await refresh();
  } else {
    makeToast();
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
  const { message } = (await $customFetch(
    `/route/anketa/files/${candId.value}`,
    {
      method: "POST",
      body: formData,
    }
  )) as Record<string, string>;
  status.value = message as "success" | "error";
  if (message == "success") {
    makeToast(message, "Файлы успешно загружены");
  } else {
    makeToast();
  }
  reset();
});

onCancel(() => {
  reset();
});

interface Pills extends TabsItem {
  slot: PillsItems | "person";
}

const items: Pills[] = [
  {
    slot: "person" as const,
    label: "Анкета",
    icon: "i-lucide-user",
  },
  {
    slot: "checks" as const,
    label: "Проверки",
    icon: "i-lucide-circle-check-big",
  },
  {
    slot: "poligrafs" as const,
    label: "Полиграф",
    icon: "i-lucide-heart-pulse",
  },
  {
    slot: "investigations" as const,
    label: "Расследования",
    icon: "i-lucide-briefcase-business",
  },
  {
    slot: "inquiries" as const,
    label: "Запросы",
    icon: "i-lucide-book-text",
  },
];
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-8">
      <USkeleton v-if="status == 'pending'" class="py-1 h-10 w-96" />
      <div v-else class="py-1">
        <h3 class="text-2xl text-red-800 font-bold">
          {{
            `${person?.surname} ${person?.firstname} ${
              person?.patronymic ?? ""
            }`
          }}
        </h3>
      </div>
      <div v-if="userState.role == 'user'" class="flex items-center space-x-4">
        <UButton
          :loading="status === 'pending'"
          variant="outline"
          icon="i-lucide-cloud-upload"
          label="Загрузить файлы"
          @click="open()"
        />
        <UButton
          :loading="status === 'pending'"
          :color="
            !person?.editable
              ? 'secondary'
              : person.user_id == userState.id
              ? 'success'
              : 'error'
          "
          :label="
            !person?.editable
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
      <template #person>
        <ContentAnketaTab
          :person="(person ? person : {} as Persons)"
          :rows="12"
          @refresh="refresh()"
        />
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
