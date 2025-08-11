<script setup lang="ts">
import { useFileDialog } from "@vueuse/core";
import type { TabsItem } from "@nuxt/ui";
import type {
  Inquisition,
  Needs,
  Persons,
  Pfo,
  PillsItems,
  Verification,
} from "@/types";

await preloadComponents(["ContentAnketaTab", "ContentSharedView"]);

const { $api } = useNuxtApp();

const route = useRoute();
const userState = useStateUser();

const candId = computed(() => route.params.id as string);
provide("candId", candId);

const {
  data: person,
  status,
  refresh,
} = await useAPI<Persons>("/route/persons/" + candId.value, {
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
  const { message } = await $api<Record<string, string>>(
    "/route/self/" + person.value?.id
  );
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
  const { message } = await $api<Record<string, string>>(
    `/route/files/${candId.value}`,
    {
      method: "POST",
      body: formData,
    }
  );
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

const items = [
  {
    label: "Анкета",
    icon: "i-lucide-user",
    slot: "person" as const,
  },
  {
    label: "Проверки",
    icon: "i-lucide-circle-check-big",
    slot: "checks" as const,
  },
  {
    label: "Полиграф",
    icon: "i-lucide-heart-pulse",
    slot: "poligrafs" as const,
  },
  {
    label: "Расследования",
    icon: "i-lucide-briefcase-business",
    slot: "investigations" as const,
  },
  {
    label: "Запросы",
    icon: "i-lucide-book-text",
    slot: "inquiries" as const,
  },
] satisfies Pills[];
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
          @refresh="refresh()"
        />
      </template>

      <template #checks="{ item }">
        <ContentSharedView :view="item.slot" :rows="16">
          <template #item="{ itemContent }">
            <ItemsCheckItem :item="itemContent as Verification" />
          </template>

          <template #form="{ formContent, submitItem }">
            <FormsCheckForm
              :item="formContent as Verification"
              @update="submitItem"
            />
          </template>
        </ContentSharedView>
      </template>

      <template #poligrafs="{ item }">
        <ContentSharedView :view="item.slot" :rows="4">
          <template #item="{ itemContent }">
            <ItemsPoligrafItem :item="itemContent as Pfo" />
          </template>

          <template #form="{ formContent, submitItem }">
            <FormsPoligrafForm
              :item="formContent as Pfo"
              @update="submitItem"
            />
          </template>
        </ContentSharedView>
      </template>

      <template #investigations="{ item }">
        <ContentSharedView :view="item.slot" :rows="3">
          <template #item="{ itemContent }">
            <ItemsInquestItem :item="itemContent as Inquisition" />
          </template>

          <template #form="{ formContent, submitItem }">
            <FormsInquestForm
              :item="formContent as Inquisition"
              @update="submitItem"
            />
          </template>
        </ContentSharedView>
      </template>

      <template #inquiries="{ item }">
        <ContentSharedView :view="item.slot" :rows="3">
          <template #item="{ itemContent }">
            <ItemsInquiryItem :item="itemContent as Needs" />
          </template>

          <template #form="{ formContent, submitItem }">
            <FormsInquiryForm
              :item="formContent as Needs"
              @update="submitItem"
            />
          </template>
        </ContentSharedView>
      </template>
    </UTabs>
  </div>
</template>
