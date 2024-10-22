<script setup lang="ts">
import type { Persons } from "@/types/interfaces";
import { watchDebounced, useFileDialog, useDateFormat } from "@vueuse/core";

const authFetch = useFetchAuth();
const userState = useUserState();
const toast = useToast();

const candidates = ref([] as Persons[]);
const page = ref(1);
const hasNext = ref(false);
const upload = ref(false);
const search = ref("");
const updated = ref("Данные обновляются...");

const { refresh, status } = await useLazyAsyncData("candidates", async () => {
  [candidates.value, hasNext.value] = (await authFetch(
    "/api/index/" + page.value,
    {
      params: {
        search: search.value,
      },
    }
  )) as [Persons[], boolean];
  updated.value = useDateFormat(useNow(), "DD.MM.YYYY в HH:mm").value;
}, {
    watch: [page]
  }
);

watchDebounced(
  () => search.value,
  () => {
    page.value = 1;
    refresh();
  },
  {
    debounce: 1000,
    maxWait: 2000,
  }
);

const { open, reset, onCancel, onChange } = useFileDialog({
  accept: ".json",
  multiple: false,
});

onChange(async (files) => {
  if (!files) return;
  upload.value = true;
  const formData = new FormData();
  formData.append("file", files[0]);
  const { person_id } = (await authFetch("/api/json", {
    method: "POST",
    body: formData,
  })) as Record<string, string>;
  reset();
  upload.value = false;
  if (person_id) {
    await refresh();
    return navigateTo("/profile/" + person_id);
  } else {
    toast.add({
      icon: "i-heroicons-information-circle",
      title: "Внимание",
      description: "Файл не был загружен",
      color: "red",
    });
  }
});

onCancel(() => {
  reset();
});

preloadRouteComponents("/profile/[id]");
</script>

<template>
  <div>
    <div v-if="userState.role == 'user'" class="relative">
      <div class="absolute inset-y-0 right-0">
        <UButton
          :loading="status == 'pending' || upload"
          :disabled="status == 'pending' || upload"
          icon="i-heroicons-cloud-arrow-up"
          title="Загрузить json файл"
          size="xl"
          variant="ghost"
          @click="open"
        />
      </div>
    </div>
    <ElementsHeaderDiv :header="'КАНДИДАТЫ'" />
    <div class="my-6">
      <UInput
        v-model="search"
        placeholder="поиск по фамилии, имени, отчеству"
      />
    </div>
    <UTable
      :loading="status == 'pending' || upload"
      :progress="{ color: 'red', animation: 'swing' }"
      :empty-state="{
        icon: 'i-heroicons-circle-stack-20-solid',
        label: 'Данные не найдены.',
      }"
      :columns="[
        { key: 'id', label: '#' },
        { key: 'region', label: 'Регион' },
        { key: 'surname', label: 'Фамилия Имя Отчество' },
        { key: 'birthday', label: 'Дата рождения' },
        { key: 'inn', label: 'ИНН' },
        { key: 'snils', label: 'СНИЛС' },
        { key: 'created', label: 'Обновлено' },
        { key: 'username', label: 'Сотрудник' },
        { key: 'editable', label: 'Статус' },
      ]"
      :rows="candidates"
      @select="navigateTo(`/profile/${$event.id}`)"
    >
      <template #id-data="{ row }">{{ row.id }}</template>
      <template #region-data="{ row }">{{ row.region }}</template>
      <template #surname-data="{ row }">
        {{
          `${row.surname} ${row.firstname} ${
            row.patronymic ? row.patronymic : ""
          }`
        }}
      </template>
      <template #birthday-data="{ row }">{{
        new Date(row.birthday).toLocaleDateString()
      }}</template>
      <template #created-data="{ row }">{{
        new Date(row.created).toLocaleDateString()
      }}</template>
      <template #username-data="{ row }">{{
        row.username ? row.username.toString().split(" ")[0] : ""
      }}</template>
      <template #editable-data="{ row }">
        <div
          class="text-start"
          :class="row.editable ? 'text-red-600' : 'text-primary'"
          :title="row.editable ? 'Анкета редактируется' : 'Анкета обновлена'"
        >
          <UIcon
            :name="
              row.editable
                ? 'i-heroicons-arrow-path'
                : 'i-heroicons-check-circle'
            "
            class="w-6 h-6"
            :class="{ ' animate-spin': row.editable }"
          />
        </div>
      </template>
      <template #caption>
        <caption class="caption-bottom text-left mt-2">
          <UButton
            variant="link"
            icon="i-heroicons-arrow-path"
            :label="`Обновлено: ${updated}`"
            :loading="status == 'pending'"
            @click="refresh"
          />
        </caption>
      </template>
    </UTable>
    <div v-if="page > 1 || hasNext" class="justify-center flex pt-4">
      <UTooltip text="Предыдущая страница">
        <UButton
          icon="i-heroicons-arrow-small-left-20-solid"
          :disabled="page < 2"
          :ui="{ rounded: 'rounded-full' }"
          class="me-2"
          @click="page--"
        />
      </UTooltip>
      <UTooltip text="Следующая страница">
        <UButton
          icon="i-heroicons-arrow-small-right-20-solid"
          :disabled="!hasNext"
          :ui="{ rounded: 'rounded-full' }"
          class="ms-2"
          @click="page++"
        />
      </UTooltip>
    </div>
  </div>
</template>
